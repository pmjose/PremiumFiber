# Snowflake Intelligence Demo – PremiumFiber Spain (FTTH Infrastructure)

This repo configures a Snowflake Intelligence demo themed for **PremiumFiber**, using synthetic structured data plus reports in `unstructured_docs` to ground answers in FTTH network operations, subscriber growth, network coverage, and customer service.

## About PremiumFiber (real-world facts)
- Spain's largest fiber optic infrastructure company providing FTTH services to **12M+ homes passed** across **250+ municipalities**.
- **100% fiber optic** infrastructure using **XGS-PON technology**.
- Company: **Premium Fiber S.L.** (legal entity: Avlley Fibre S.L.)
- Created by: **MasOrange (58%)**, **Vodafone España (17%)**, **GIC (25%)**
- CEO: **Blanca Ceña** · CFO: **Rafael Casquel** · CTO: **Norberto Ojinaga**
- HQ: C/ Basauri, 5, 28023 Madrid, España

### Product Lines
**Internet Hogar (Residential):**
- 300 Mbps - €29.90/mes
- 600 Mbps - €39.90/mes (RECOMENDADO)
- 1000 Mbps (Gamer) - €49.90/mes
- Mesh Plus - €59.90/mes (includes Mesh WiFi 6)

**Internet Empresas (Business):**
- Professional 600 Mbps (simétrico)
- Business 1000 Mbps
- Enterprise 1000 Mbps (simétrico)

**Equipment:** WiFi 5, WiFi 6, Mesh routers

**Services:** IP Pública Fija, Firewall, Monitoreo 24/7, SLA empresarial

### Contact
- **Hogar**: +34 91 123 4567
- **Empresas**: +34 91 234 5678
- Website: [premiumfiber.es](https://www.premiumfiber.es/)

## What's included
- **SQL setup script**: `sql_scripts/01_demo_setup.sql` builds `PREMIUMFIBER_AI_DEMO` and loads sample data + documents into stages.
- **Structured sample data** (`demo_data/`): synthetic fact/dim tables to model revenue, subscriber metrics, service performance, campaigns, and workforce. Segments reflect PremiumFiber's business (Residential, Enterprise).
- **Unstructured reports** (`unstructured_docs/`): narrative files used by Cortex Search. Notable references:
  - Finance: Financial reports, revenue mix, subscriber growth, ARPU analysis.
  - Strategy: Board presentations, market position, competitive analysis.
  - Network: Fiber coverage, network performance, expansion plans.
  - Demo: Demo scripts for CEO, CFO, CMO personas.

## Quick start
1. Open `sql_scripts/01_demo_setup.sql` in a Snowflake worksheet (use `ACCOUNTADMIN` to create integrations, then the `PREMIUMFIBER_DEMO` role created by the script).
2. Run the script end-to-end to create the database, schema, stage, load CSVs, and register Cortex Search services and the `PREMIUMFIBER_EXECUTIVE_AGENT`.
3. Verify objects:
   - `SHOW TABLES IN PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA;`
   - `SHOW SEMANTIC VIEWS;`
   - `SHOW CORTEX SEARCH SERVICES;`

## Suggested prompts (FTTH context)
- **Subscriber metrics**: "What is our total subscriber count by region and plan type?"
- **Revenue & ARPU**: "Show monthly recurring revenue (MRR) and ARPU trends by segment."
- **Product performance**: "Which internet plans have the highest adoption?"
- **Churn analysis**: "What is our churn rate by plan type and region?"
- **Marketing ROI**: "Which marketing campaigns generated the most new subscribers?"
- **Competitive position**: "How do we compare against Telefónica and Digi?"

## Personas
- **CEO**: Strategy, subscriber growth, market share, competitive position.
- **CFO**: Revenue, ARPU, churn, MRR/ARR, cost per acquisition.
- **COO/CTO**: Network coverage, fiber deployment, uptime SLAs, capacity planning.
- **CMO**: Campaign performance, lead generation, brand awareness, customer acquisition cost.

## Notes
- Structured data is synthetic but aligned to FTTH business metrics; unstructured reports supply realistic narrative context.
- Update or replace CSVs/documents as needed—`sql_scripts/01_demo_setup.sql` will stage whatever is present in `demo_data/` and `unstructured_docs/`.
- Guardrails in the agent are tuned to only answer questions about PremiumFiber's business (FTTH infrastructure, network coverage, customer service).
- Currency is **Euros (€)** throughout.
