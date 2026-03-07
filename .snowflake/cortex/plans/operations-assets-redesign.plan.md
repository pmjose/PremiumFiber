---
name: "operations-assets-redesign"
created: "2026-03-07T10:56:18.759Z"
status: pending
---

# Plan: Redesign Operations & Assets for Billing Reconciliation

## Current State

The Operations & Assets section in streamlit\_app.py (lines 8770-10200+) currently has 3 tabs:

1. Invoice & PO Tracking (vendor procurement focus)
2. Fixed Asset Inventory (generic asset categories)
3. Amortization & Depreciation (financial controls)

**Problem**: This structure does NOT tell PremiumFiber's billing reconciliation story. It focuses on vendor procurement rather than the core pain point: weekly billing committees with Vodafone/MasOrange due to inventory mismatches.

## Target Architecture

```
flowchart TB
    subgraph ops [Operations & Assets Section]
        T1[Network Topology]
        T2[Service Inventory]
        T3[Partner Orders]
        T4[Billing Reconciliation]
        T5[Asset Amortization]
    end
    
    subgraph data [Data Entities]
        NE[Network Elements]
        SI[Service Inventory]
        PO[Partner Orders]
        PIV[Partner Inventory View]
        AR[Asset Register]
    end
    
    T1 --> NE
    T2 --> SI
    T3 --> PO
    T4 --> SI
    T4 --> PIV
    T5 --> AR
    T5 --> SI
    
    SI -->|compare| PIV
    PIV -->|orphan/ghost| T4
```

## Implementation Tasks

### Task 1: Restructure Tabs and Add Network Topology

**Location**: Lines 8804-8808

**Current code**:

```
ops_tab_invoices, ops_tab_assets, ops_tab_amortization = st.tabs([
    "Invoice & PO Tracking",
    "Fixed Asset Inventory",
    "Amortization & Depreciation",
])
```

**New structure**:

```
tab_topology, tab_inventory, tab_orders, tab_recon, tab_amort = st.tabs([
    "Network Topology",
    "Service Inventory",
    "Partner Orders",
    "Billing Reconciliation",
    "Asset Amortization",
])
```

**Network Topology tab content**:

- Header: "Fiber Access Network - OLT to Home"
- KPIs: Total OLTs, PON ports, Splitters, Homes passed, Homes connected
- Visualization: Hierarchical view showing OLT > PON Port > Splitter > Distribution > Home
- Sample data structure:

```
network_elements = pd.DataFrame({
    "Element ID": ["OLT-MAD-001", "PON-MAD-001-01", "SPL-MAD-001-01-A", ...],
    "Type": ["OLT", "PON Port", "Splitter 1:32", "Distribution Point", ...],
    "Parent": [None, "OLT-MAD-001", "PON-MAD-001-01", ...],
    "Capacity": [16, 32, 32, 8, ...],
    "Used": [14, 28, 24, 6, ...],
    "Location": ["Madrid Central", "Madrid Central", "Chamartin", ...],
})
```

---

### Task 2: Create Service Inventory Tab (Core)

**This is the central tab for the billing reconciliation story.**

**Data model**:

```
service_inventory = pd.DataFrame({
    "Service ID": ["SVC-2024-000001", "SVC-2024-000002", ...],
    "Partner": ["MasOrange", "Vodafone", "MasOrange", ...],
    "Address": ["Calle Gran Via 42, 3A, Madrid", ...],
    "OLT": ["OLT-MAD-001", ...],
    "PON Port": ["PON-MAD-001-01", ...],
    "Bandwidth": ["1Gbps", "600Mbps", "300Mbps", ...],
    "Status": ["Active", "Active", "Pending Disconnect", ...],
    "Activation Date": ["2023-06-15", ...],
    "Deactivation Date": [None, None, "2025-03-15", ...],
    "MRC EUR": [15.50, 12.00, 15.50, ...],
    "Last Sync": ["2025-03-07", ...],
})
```

**UI elements**:

1. KPI header: Total active lines, Lines by partner (MO/VF split), MRC total, Avg bandwidth
2. Filter by: Partner, Status, OLT, Date range
3. Data table with service details
4. Chart: Lines by partner (pie), Lines by bandwidth tier (bar), Activation trend (line)
5. AI recommendation: Service concentration risks, capacity alerts

---

### Task 3: Add Orphan/Ghost Line Detection

**Location**: Enhance Billing Reconciliation tab (currently lines 9436-9670)

**New data structures**:

```
# PremiumFiber's view
pf_inventory = service_inventory.copy()

# Partner's view (simulated from their system)
partner_inventory = pd.DataFrame({
    "Partner Line ID": ["MO-LINE-00001", "VF-LINE-00001", ...],
    "Partner": ["MasOrange", "Vodafone", ...],
    "PF Service ID": ["SVC-2024-000001", None, ...],  # None = ghost line
    "Address": [...],
    "Status": ["Active", "Active", ...],
    "Partner Activation Date": ["2023-06-15", "2023-05-01", ...],
    "Partner MRC EUR": [15.50, 12.00, ...],
})

# Reconciliation result
recon_result = pd.DataFrame({
    "Service ID": [...],
    "Partner": [...],
    "Discrepancy Type": ["Orphan", "Ghost", "Lifecycle Mismatch", "Rate Mismatch", "Matched"],
    "PF Status": [...],
    "Partner Status": [...],
    "PF Activation": [...],
    "Partner Activation": [...],
    "Billing Impact EUR": [15.50, -12.00, 3.00, ...],
    "Root Cause": ["Partner disconnect not processed", "Missing activation in PF", ...],
})
```

**UI elements**:

1. KPI header: Matched lines, Orphan count (+ EUR impact), Ghost count (+ EUR impact), Lifecycle mismatches
2. Visual: Venn diagram style showing overlap/gaps
3. Discrepancy table with filters by type, partner, impact
4. Drill-down: Click discrepancy to see service detail
5. AI recommendation: "47 orphan lines represent EUR 728/month overbilling to MasOrange. Recommend joint audit with partner."

---

### Task 4: Refactor Partner Orders Tab

**Location**: Refactor from current Tenant Service Orders (lines 9114-9386)

**Keep**: MasOrange/Vodafone branding, order tracking, SLA status **Remove**: Generic procurement language **Add**: Billing impact per order

**Enhanced data**:

```
partner_orders = pd.DataFrame({
    "Order ID": ["ORD-MO-2025-001", ...],
    "Partner": ["MasOrange", "Vodafone", ...],
    "Order Type": ["Connect", "Modify", "Cease", ...],
    "Service ID": ["SVC-2024-000001", ...],  # Link to inventory
    "Address": [...],
    "Requested Date": [...],
    "SLA Deadline": [...],
    "Completed Date": [...],
    "Status": ["Completed", "In Progress", "Pending", ...],
    "Billing Impact": ["New MRC +15.50", "Bandwidth upgrade +3.00", "MRC stop -15.50", ...],
    "Inventory Updated": ["Yes", "Pending", "No", ...],
})
```

**Key addition**: "Inventory Updated" flag shows whether the order has been reflected in Service Inventory - mismatches here cause billing disputes.

---

### Task 5: Link Asset Amortization to Services

**Location**: Refactor current Amortization tab (lines 9977-10200+)

**Add linkage to billable services**:

```
asset_service_link = pd.DataFrame({
    "Asset ID": ["OLT-MAD-001", "SPL-MAD-001-01-A", ...],
    "Asset Type": ["OLT", "Splitter", ...],
    "Gross Value EUR": [125000, 450, ...],
    "Net Book Value EUR": [78000, 280, ...],
    "Depreciation Pct": [37.6, 37.8, ...],
    "Status": ["In Service", "Decommissioned", ...],
    "Services Supported": [892, 0, ...],  # Active lines on this asset
    "Monthly MRC Generated": [13826, 0, ...],
    "Flag": [None, "Decommissioned but still in billing", ...],
})
```

**New insights**:

- "12 decommissioned splitters still linked to 48 active services - billing anomaly"
- "OLT-BCN-003 is 85% depreciated but supports EUR 24K/month MRC - capex refresh candidate"

---

### Task 6: Remove Irrelevant Content

**Remove or significantly reduce**:

| Current Content             | Location        | Action                                   |
| --------------------------- | --------------- | ---------------------------------------- |
| Purchase Order Pipeline     | Lines 8848-9113 | Remove - vendor procurement not relevant |
| Vendor Performance tab      | Lines 9751-9801 | Remove - tracks Nokia/Huawei, not VF/MO  |
| 3-Way Match (PO/GR/Invoice) | Lines 9387-9435 | Remove - internal procurement process    |
| Generic Invoice Processing  | Lines 9387-9516 | Reduce - keep only tenant billing        |

**Keep and enhance**:

- Tenant Billing Reconciliation (lines 9518-9670) - move to main Billing Reconciliation tab
- IFRS 15 Revenue Recognition (lines 9672-9749) - keep as sub-section

---

## File Changes Summary

| File              | Lines Affected | Change Type                    |
| ----------------- | -------------- | ------------------------------ |
| streamlit\_app.py | 8804-8808      | Restructure tabs               |
| streamlit\_app.py | 8810-9113      | Replace with Network Topology  |
| streamlit\_app.py | 9114-9386      | Refactor to Partner Orders     |
| streamlit\_app.py | 9387-9750      | Replace with Service Inventory |
| streamlit\_app.py | 9751-9801      | Remove Vendor Performance      |
| streamlit\_app.py | 9804-9975      | Refactor Asset Amortization    |
| streamlit\_app.py | 9977-10200     | Link to services               |

**Estimated scope**: \~1500 lines modified/replaced

---

## Success Criteria

1. Service Inventory is the central, visible data model
2. Orphan/Ghost lines are explicitly shown with EUR impact
3. Partner orders clearly link to inventory changes and billing impact
4. Asset depreciation links to billable services
5. All content is specific to PremiumFiber/VF/MO context (no generic procurement)
6. Demo tells the story: "We know what we own, what services run on it, and what partners should pay"
