# Plan: Operations and Assets Agent Data Setup

## Overview

Enable your existing Snowflake Intelligence agent to answer questions about the Operations and Assets dashboard by creating the required tables, loading data, and creating semantic views.

## Current State Analysis

**Existing Setup:**
- Database: `PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA`
- Existing semantic view: `PF_WHOLESALE_SEMANTIC_VIEW` (covers partners, revenue, SLA, network)
- Existing tables: Finance, HR, Marketing, Sales, Wholesale data
- Cortex Search: Document store in `PF_INTERNAL_STAGE`

**Missing for Operations and Assets:**
The dashboard displays mock data that does not exist in Snowflake. We need to create tables for:
1. Service Inventory (892K lines, OLT assignments, partner splits)
2. Billing Discrepancies (orphans, ghosts, lifecycle drift)
3. Partner Orders (connect/modify/cease workflows)
4. Asset Register (depreciation, NBV, service linkage)
5. Asset Failure Predictions (ML outputs)
6. Reconciliation Anomalies (ML-detected patterns)

---

## Task 1: Create Operations Tables

Create the following tables in `PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA`:

```sql
-- 1. Service Inventory (Network elements and active services)
CREATE OR REPLACE TABLE PF_SERVICE_INVENTORY (
    SERVICE_ID VARCHAR(20) PRIMARY KEY,
    PARTNER VARCHAR(20),          -- MasOrange, Vodafone
    ADDRESS VARCHAR(200),
    OLT_ID VARCHAR(20),
    PON_PORT VARCHAR(10),
    BANDWIDTH VARCHAR(20),        -- 300 Mbps, 600 Mbps, 1 Gbps
    STATUS VARCHAR(20),           -- Active, Pending Activation, Pending Disconnect
    ACTIVATION_DATE DATE,
    MRC_EUR NUMBER(10,2),
    REGION VARCHAR(50)
);

-- 2. Billing Discrepancies
CREATE OR REPLACE TABLE PF_BILLING_DISCREPANCIES (
    DISCREPANCY_ID VARCHAR(20) PRIMARY KEY,
    SERVICE_ID VARCHAR(20),
    PARTNER VARCHAR(20),
    DISCREPANCY_TYPE VARCHAR(30), -- Orphan, Ghost, Lifecycle Mismatch
    PF_STATUS VARCHAR(20),
    PARTNER_STATUS VARCHAR(20),
    PF_ACTIVATION_DATE DATE,
    PARTNER_ACTIVATION_DATE DATE,
    PF_DEACTIVATION_DATE DATE,
    PARTNER_DEACTIVATION_DATE DATE,
    MRC_IMPACT_EUR NUMBER(10,2),
    ROOT_CAUSE VARCHAR(200),
    DAYS_OUTSTANDING INTEGER,
    CREATED_DATE DATE
);

-- 3. Partner Orders
CREATE OR REPLACE TABLE PF_PARTNER_ORDERS (
    ORDER_ID VARCHAR(30) PRIMARY KEY,
    PARTNER VARCHAR(20),
    ORDER_TYPE VARCHAR(20),       -- Connect, Modify, Cease
    SERVICE_ID VARCHAR(20),
    ADDRESS VARCHAR(200),
    BANDWIDTH VARCHAR(50),        -- Can include transitions like "600 Mbps -> 1 Gbps"
    ORDER_DATE DATE,
    SLA_DEADLINE DATE,
    STATUS VARCHAR(20),           -- In Progress, Completed, Pending
    BILLING_IMPACT VARCHAR(20),
    INVENTORY_UPDATED VARCHAR(10)
);

-- 4. Asset Register (linked to services)
CREATE OR REPLACE TABLE PF_ASSET_REGISTER (
    ASSET_ID VARCHAR(30) PRIMARY KEY,
    ASSET_TYPE VARCHAR(50),       -- OLT Chassis, Splitter 1:32, Fiber Trunk, etc.
    LOCATION VARCHAR(100),
    GROSS_VALUE_EUR NUMBER(12,2),
    NET_BOOK_VALUE_EUR NUMBER(12,2),
    DEPRECIATION_PCT NUMBER(5,2),
    STATUS VARCHAR(20),           -- In Service, Decommissioned, Failed
    SERVICES_SUPPORTED INTEGER,
    MONTHLY_MRC_EUR NUMBER(12,2),
    USEFUL_LIFE_YEARS INTEGER,
    ACQUISITION_DATE DATE,
    DECOMMISSION_DATE DATE
);

-- 5. Asset Failure Predictions (ML outputs)
CREATE OR REPLACE TABLE PF_ASSET_FAILURE_PREDICTIONS (
    PREDICTION_ID VARCHAR(20) PRIMARY KEY,
    ASSET_ID VARCHAR(30),
    ASSET_TYPE VARCHAR(50),
    FAILURE_PROBABILITY NUMBER(5,2),
    PREDICTED_WINDOW VARCHAR(20), -- 7-14 days, 15-30 days, etc.
    SERVICES_AT_RISK INTEGER,
    MRC_AT_RISK_EUR NUMBER(10,2),
    REPLACEMENT_COST_EUR NUMBER(10,2),
    PREDICTION_DATE DATE,
    OPTIMAL_ACTION VARCHAR(30),   -- Replace Now, Schedule Q2, Monitor
    ROI_IF_REPLACED VARCHAR(20),
    PAYBACK_MONTHS INTEGER
);

-- 6. Reconciliation Anomalies (ML-detected)
CREATE OR REPLACE TABLE PF_RECONCILIATION_ANOMALIES (
    ANOMALY_ID VARCHAR(20) PRIMARY KEY,
    PATTERN VARCHAR(100),
    AFFECTED_LINES INTEGER,
    CONFIDENCE NUMBER(5,2),
    MRC_IMPACT_EUR NUMBER(10,2),
    DETECTION_DATE DATE,
    STATUS VARCHAR(20),           -- New, Investigating, Confirmed, Resolved
    ROOT_CAUSE_CATEGORY VARCHAR(50)
);

-- 7. Network Elements (OLTs)
CREATE OR REPLACE TABLE PF_NETWORK_ELEMENTS (
    ELEMENT_ID VARCHAR(20) PRIMARY KEY,
    LOCATION VARCHAR(100),
    VENDOR VARCHAR(50),
    PON_PORTS_TOTAL INTEGER,
    PON_PORTS_USED INTEGER,
    SPLITTERS INTEGER,
    HOMES_CONNECTED INTEGER,
    MO_LINES INTEGER,
    VF_LINES INTEGER,
    UTILIZATION_PCT NUMBER(5,2)
);
```

---

## Task 2: Load Mock Data

Insert the dashboard mock data into the tables. Example for discrepancies:

```sql
INSERT INTO PF_BILLING_DISCREPANCIES VALUES
('DISC-001', 'SVC-2024-234567', 'MasOrange', 'Orphan', 'Active', NULL, '2023-06-15', NULL, NULL, NULL, 15.50, 'Disconnect not synced to MO', 45, CURRENT_DATE),
('DISC-002', 'SVC-2024-345678', 'Vodafone', 'Ghost', NULL, 'Active', NULL, '2023-06-15', NULL, NULL, -12.00, 'Missing in PF OSS', 12, CURRENT_DATE),
-- ... (all rows from dashboard)
```

Similar inserts for all other tables based on the DataFrame definitions in [streamlit_app.py](streamlit_app/streamlit_app.py) lines 8840-10070.

---

## Task 3: Create PF_OPERATIONS_SEMANTIC_VIEW

```sql
CREATE OR REPLACE SEMANTIC VIEW PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_OPERATIONS_SEMANTIC_VIEW
  COMMENT = 'PremiumFiber Operations semantic view - billing reconciliation, service inventory, partner orders, and discrepancy management for wholesale fiberco operations'
  TABLES (
    SERVICE_INVENTORY (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_SERVICE_INVENTORY'
      PRIMARY_KEY = (SERVICE_ID)
      DIMENSIONS (
        PARTNER COMMENT = 'Wholesale partner: MasOrange or Vodafone'
        STATUS COMMENT = 'Service status: Active, Pending Activation, Pending Disconnect'
        BANDWIDTH COMMENT = 'Service bandwidth tier: 300 Mbps, 600 Mbps, 1 Gbps'
        OLT_ID COMMENT = 'OLT equipment identifier'
        REGION COMMENT = 'Geographic region'
      )
      FACTS (
        MRC_EUR COMMENT = 'Monthly Recurring Charge in EUR'
      )
      METRICS (
        TOTAL_MRC AS SUM(MRC_EUR) COMMENT = 'Total MRC across services'
        ACTIVE_LINES AS COUNT_IF(STATUS = ''Active'') COMMENT = 'Count of active service lines'
      )
    )
    DISCREPANCIES (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_BILLING_DISCREPANCIES'
      PRIMARY_KEY = (DISCREPANCY_ID)
      DIMENSIONS (
        DISCREPANCY_TYPE COMMENT = 'Type: Orphan (in PF not partner), Ghost (in partner not PF), Lifecycle Mismatch'
        PARTNER COMMENT = 'Affected partner'
        ROOT_CAUSE COMMENT = 'Identified root cause of discrepancy'
      )
      FACTS (
        MRC_IMPACT_EUR COMMENT = 'MRC impact in EUR (positive=at risk, negative=unbilled)'
        DAYS_OUTSTANDING COMMENT = 'Days since discrepancy detected'
      )
      METRICS (
        ORPHAN_COUNT AS COUNT_IF(DISCREPANCY_TYPE = ''Orphan'') COMMENT = 'Lines in PF but not in partner system'
        GHOST_COUNT AS COUNT_IF(DISCREPANCY_TYPE = ''Ghost'') COMMENT = 'Lines in partner but not in PF'
        TOTAL_MRC_AT_RISK AS SUM(CASE WHEN MRC_IMPACT_EUR > 0 THEN MRC_IMPACT_EUR ELSE 0 END)
      )
    )
    PARTNER_ORDERS (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_PARTNER_ORDERS'
      PRIMARY_KEY = (ORDER_ID)
      DIMENSIONS (
        ORDER_TYPE COMMENT = 'Order type: Connect, Modify, Cease'
        PARTNER COMMENT = 'Ordering partner'
        STATUS COMMENT = 'Order status'
      )
    )
    ANOMALIES (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_RECONCILIATION_ANOMALIES'
      PRIMARY_KEY = (ANOMALY_ID)
      DIMENSIONS (
        PATTERN COMMENT = 'ML-detected anomaly pattern'
        STATUS COMMENT = 'Investigation status'
      )
      FACTS (
        CONFIDENCE COMMENT = 'ML confidence score (0-100)'
        AFFECTED_LINES COMMENT = 'Number of lines affected'
      )
    )
    NETWORK_ELEMENTS (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_NETWORK_ELEMENTS'
      PRIMARY_KEY = (ELEMENT_ID)
    )
  );
```

---

## Task 4: Create PF_ASSET_SEMANTIC_VIEW

```sql
CREATE OR REPLACE SEMANTIC VIEW PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_ASSET_SEMANTIC_VIEW
  COMMENT = 'PremiumFiber Asset Management semantic view - depreciation, NBV, service linkage, and predictive maintenance for network assets'
  TABLES (
    ASSETS (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_ASSET_REGISTER'
      PRIMARY_KEY = (ASSET_ID)
      DIMENSIONS (
        ASSET_TYPE COMMENT = 'Asset category: OLT Chassis, Splitter, Fiber Trunk, etc.'
        STATUS COMMENT = 'Asset status: In Service, Decommissioned, Failed'
        LOCATION COMMENT = 'Physical location'
      )
      FACTS (
        GROSS_VALUE_EUR COMMENT = 'Original asset cost in EUR'
        NET_BOOK_VALUE_EUR COMMENT = 'Current book value after depreciation'
        DEPRECIATION_PCT COMMENT = 'Percentage depreciated'
        SERVICES_SUPPORTED COMMENT = 'Number of service lines supported by this asset'
        MONTHLY_MRC_EUR COMMENT = 'Monthly revenue generated from services on this asset'
      )
      METRICS (
        TOTAL_NBV AS SUM(NET_BOOK_VALUE_EUR) COMMENT = 'Total Net Book Value'
        TOTAL_GROSS AS SUM(GROSS_VALUE_EUR) COMMENT = 'Total Gross Value'
        MRC_PER_NBV AS SUM(MONTHLY_MRC_EUR) / NULLIF(SUM(NET_BOOK_VALUE_EUR), 0) COMMENT = 'Revenue efficiency ratio'
      )
    )
    FAILURE_PREDICTIONS (
      BASE_TABLE = 'PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_ASSET_FAILURE_PREDICTIONS'
      PRIMARY_KEY = (PREDICTION_ID)
      DIMENSIONS (
        OPTIMAL_ACTION COMMENT = 'Recommended action: Replace Now, Schedule Q2, Monitor'
        PREDICTED_WINDOW COMMENT = 'Predicted failure timeframe'
      )
      FACTS (
        FAILURE_PROBABILITY COMMENT = 'ML-predicted failure probability (0-100)'
        SERVICES_AT_RISK COMMENT = 'Lines that would be affected by failure'
        MRC_AT_RISK_EUR COMMENT = 'Revenue at risk if asset fails'
      )
      METRICS (
        HIGH_RISK_ASSETS AS COUNT_IF(FAILURE_PROBABILITY >= 70) COMMENT = 'Assets with 70%+ failure risk'
        TOTAL_MRC_AT_RISK AS SUM(MRC_AT_RISK_EUR) COMMENT = 'Total MRC at risk from predicted failures'
      )
    )
  );
```

---

## Task 5: Update Agent Configuration

Add the new semantic views to your Snowflake Intelligence agent. In Snowsight:

1. Navigate to **AI and ML > Snowflake Intelligence**
2. Edit your existing agent
3. Add data sources:
   - `PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_OPERATIONS_SEMANTIC_VIEW`
   - `PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA.PF_ASSET_SEMANTIC_VIEW`
4. Update the agent's system prompt to include Operations and Assets context

**Suggested system prompt addition:**
```
You can also answer questions about PremiumFiber wholesale operations including:
- Billing reconciliation: orphan lines, ghost lines, lifecycle drift discrepancies
- Service inventory: active lines by partner (MasOrange, Vodafone), bandwidth tiers, OLT assignments
- Partner orders: connect/modify/cease workflows, SLA compliance
- Asset management: depreciation schedules, net book value, service linkage
- Predictive maintenance: ML-predicted asset failures, replacement recommendations
```

---

## Data Schema Summary

| Domain | Table | Key Metrics |
|--------|-------|-------------|
| Service Inventory | PF_SERVICE_INVENTORY | 892K lines, MRC by partner |
| Billing Reconciliation | PF_BILLING_DISCREPANCIES | Orphans, ghosts, lifecycle drift |
| Partner Orders | PF_PARTNER_ORDERS | Connect/modify/cease by partner |
| Asset Register | PF_ASSET_REGISTER | NBV, depreciation, service linkage |
| Failure Predictions | PF_ASSET_FAILURE_PREDICTIONS | ML risk scores, replacement reco |
| Anomalies | PF_RECONCILIATION_ANOMALIES | ML-detected patterns |
| Network Elements | PF_NETWORK_ELEMENTS | OLT capacity, utilization |

---

## Example Questions the Agent Will Answer

After implementation, your agent will be able to answer:

1. **Billing Reconciliation:**
   - "How many orphan lines do we have with MasOrange?"
   - "What is the total MRC at risk from billing discrepancies?"
   - "Show me ghost lines older than 30 days"

2. **Service Inventory:**
   - "How many active lines does Vodafone have?"
   - "What is our MRC breakdown by bandwidth tier?"
   - "Which OLTs have the highest utilization?"

3. **Partner Orders:**
   - "How many connect orders are pending for MasOrange?"
   - "What is our SLA compliance rate this month?"
   - "Show me orders at risk of missing SLA deadline"

4. **Asset Management:**
   - "What is our total net book value?"
   - "Which assets have the best MRC efficiency?"
   - "Show me decommissioned assets still linked to services"

5. **Predictive Maintenance:**
   - "Which assets have failure probability above 70%?"
   - "What is the total MRC at risk from predicted failures?"
   - "Show me assets recommended for immediate replacement"
