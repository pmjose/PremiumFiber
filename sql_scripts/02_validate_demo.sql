-- ========================================================================
-- PremiumFiber Demo Validation Script
-- Validates all tables created, data loaded, and unstructured docs parsed
-- ========================================================================

USE ROLE PREMIUMFIBER_DEMO;
USE DATABASE PREMIUMFIBER_AI_DEMO;
USE SCHEMA PREMIUMFIBER_SCHEMA;
USE WAREHOUSE PREMIUMFIBER_DEMO_WH;

-- ========================================================================
-- SECTION 1: INFRASTRUCTURE VALIDATION
-- ========================================================================

SELECT '=== INFRASTRUCTURE VALIDATION ===' AS section;

-- Check database exists
SELECT 'Database' AS object_type, 
       DATABASE_NAME AS object_name,
       CASE WHEN DATABASE_NAME IS NOT NULL THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.DATABASES 
WHERE DATABASE_NAME = 'PREMIUMFIBER_AI_DEMO';

-- Check schema exists
SELECT 'Schema' AS object_type,
       SCHEMA_NAME AS object_name,
       CASE WHEN SCHEMA_NAME IS NOT NULL THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE SCHEMA_NAME = 'PREMIUMFIBER_SCHEMA';

-- Check warehouse exists
SHOW WAREHOUSES LIKE 'PREMIUMFIBER_DEMO_WH';

-- Check Git repository
SHOW GIT REPOSITORIES LIKE 'PREMIUMFIBER_AI_DEMO_REPO';

-- Check internal stage
SHOW STAGES LIKE 'PF_INTERNAL_STAGE';

-- ========================================================================
-- SECTION 2: DIMENSION TABLES VALIDATION
-- ========================================================================

SELECT '=== DIMENSION TABLES VALIDATION ===' AS section;

SELECT 'PF_PRODUCT_CATEGORY_DIM' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM PF_PRODUCT_CATEGORY_DIM
UNION ALL
SELECT 'PF_PRODUCT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_PRODUCT_DIM
UNION ALL
SELECT 'PF_VENDOR_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_VENDOR_DIM
UNION ALL
SELECT 'PF_CUSTOMER_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_CUSTOMER_DIM
UNION ALL
SELECT 'PF_ACCOUNT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_ACCOUNT_DIM
UNION ALL
SELECT 'PF_DEPARTMENT_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_DEPARTMENT_DIM
UNION ALL
SELECT 'PF_REGION_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_REGION_DIM
UNION ALL
SELECT 'PF_SALES_REP_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_SALES_REP_DIM
UNION ALL
SELECT 'PF_CAMPAIGN_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_CAMPAIGN_DIM
UNION ALL
SELECT 'PF_CHANNEL_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_CHANNEL_DIM
UNION ALL
SELECT 'PF_EMPLOYEE_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_EMPLOYEE_DIM
UNION ALL
SELECT 'PF_JOB_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_JOB_DIM
UNION ALL
SELECT 'PF_LOCATION_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_LOCATION_DIM
UNION ALL
SELECT 'PF_NETWORK_STATUS_DIM', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_NETWORK_STATUS_DIM
ORDER BY table_name;

-- ========================================================================
-- SECTION 3: FACT TABLES VALIDATION
-- ========================================================================

SELECT '=== FACT TABLES VALIDATION ===' AS section;

SELECT 'PF_SALES_FACT' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM PF_SALES_FACT
UNION ALL
SELECT 'PF_FINANCE_TRANSACTIONS', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_FINANCE_TRANSACTIONS
UNION ALL
SELECT 'PF_MARKETING_CAMPAIGN_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_MARKETING_CAMPAIGN_FACT
UNION ALL
SELECT 'PF_HR_EMPLOYEE_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_HR_EMPLOYEE_FACT
UNION ALL
SELECT 'PF_NETWORK_INCIDENTS_FACT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_NETWORK_INCIDENTS_FACT
UNION ALL
SELECT 'PF_NETWORK_MAINTENANCE_SCHEDULE', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_NETWORK_MAINTENANCE_SCHEDULE
ORDER BY table_name;

-- ========================================================================
-- SECTION 4: SALESFORCE TABLES VALIDATION
-- ========================================================================

SELECT '=== SALESFORCE TABLES VALIDATION ===' AS section;

SELECT 'PF_SF_ACCOUNTS' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END AS status 
FROM PF_SF_ACCOUNTS
UNION ALL
SELECT 'PF_SF_OPPORTUNITIES', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_SF_OPPORTUNITIES
UNION ALL
SELECT 'PF_SF_CONTACTS', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ LOADED' ELSE '✗ EMPTY' END 
FROM PF_SF_CONTACTS
ORDER BY table_name;

-- ========================================================================
-- SECTION 5: UNSTRUCTURED DATA VALIDATION
-- ========================================================================

SELECT '=== UNSTRUCTURED DATA VALIDATION ===' AS section;

-- Check files in internal stage
SELECT 'Files in PF_INTERNAL_STAGE' AS check_type;
SELECT COUNT(*) AS file_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ FILES PRESENT' ELSE '✗ NO FILES' END AS status
FROM DIRECTORY(@PF_INTERNAL_STAGE);

-- List unstructured doc files
SELECT 'Unstructured Documents' AS check_type;
SELECT relative_path, size, last_modified
FROM DIRECTORY(@PF_INTERNAL_STAGE)
WHERE relative_path ILIKE 'unstructured_docs/%'
ORDER BY relative_path;

-- Check parsed content tables
SELECT 'PF_PARSED_CONTENT_DOCS' AS table_name, COUNT(*) AS row_count, 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END AS status 
FROM PF_PARSED_CONTENT_DOCS
UNION ALL
SELECT 'PF_PARSED_CONTENT_MD', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END 
FROM PF_PARSED_CONTENT_MD
UNION ALL
SELECT 'PF_PARSED_CONTENT', COUNT(*), 
       CASE WHEN COUNT(*) > 0 THEN '✓ PARSED' ELSE '✗ EMPTY' END 
FROM PF_PARSED_CONTENT
ORDER BY table_name;

-- Show parsed document details
SELECT 'Parsed Documents Detail' AS check_type;
SELECT relative_path, LENGTH(content) AS content_length
FROM PF_PARSED_CONTENT
ORDER BY relative_path;

-- ========================================================================
-- SECTION 6: SEMANTIC VIEWS VALIDATION
-- ========================================================================

SELECT '=== SEMANTIC VIEWS VALIDATION ===' AS section;

SHOW SEMANTIC VIEWS IN SCHEMA PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA;

-- Validate each semantic view exists
SELECT 'Semantic View Check' AS check_type;
SELECT 'PF_FINANCE_SEMANTIC_VIEW' AS view_name, 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END AS status
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' AND TABLE_NAME = 'PF_FINANCE_SEMANTIC_VIEW'
UNION ALL
SELECT 'PF_SALES_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' AND TABLE_NAME = 'PF_SALES_SEMANTIC_VIEW'
UNION ALL
SELECT 'PF_MARKETING_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' AND TABLE_NAME = 'PF_MARKETING_SEMANTIC_VIEW'
UNION ALL
SELECT 'PF_HR_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' AND TABLE_NAME = 'PF_HR_SEMANTIC_VIEW'
UNION ALL
SELECT 'PF_INFRASTRUCTURE_SEMANTIC_VIEW', 
       CASE WHEN COUNT(*) > 0 THEN '✓ EXISTS' ELSE '✗ MISSING' END
FROM INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' AND TABLE_NAME = 'PF_INFRASTRUCTURE_SEMANTIC_VIEW';

-- ========================================================================
-- SECTION 7: CORTEX SEARCH SERVICES VALIDATION
-- ========================================================================

SELECT '=== CORTEX SEARCH SERVICES VALIDATION ===' AS section;

SHOW CORTEX SEARCH SERVICES IN SCHEMA PREMIUMFIBER_AI_DEMO.PREMIUMFIBER_SCHEMA;

-- ========================================================================
-- SECTION 8: GEOSPATIAL DATA VALIDATION
-- ========================================================================

SELECT '=== GEOSPATIAL DATA VALIDATION ===' AS section;

-- Check customers have lat/long
SELECT 'Customers with Geospatial' AS check_type,
       COUNT(*) AS total_customers,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM PF_CUSTOMER_DIM;

-- Check regions have lat/long
SELECT 'Regions with Geospatial' AS check_type,
       COUNT(*) AS total_regions,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM PF_REGION_DIM;

-- Check locations have lat/long
SELECT 'Locations with Geospatial' AS check_type,
       COUNT(*) AS total_locations,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM PF_LOCATION_DIM;

-- Check network nodes have lat/long
SELECT 'Network Nodes with Geospatial' AS check_type,
       COUNT(*) AS total_nodes,
       SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) AS with_coordinates,
       ROUND(100.0 * SUM(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_complete
FROM PF_NETWORK_STATUS_DIM;

-- ========================================================================
-- SECTION 9: DATA QUALITY CHECKS
-- ========================================================================

SELECT '=== DATA QUALITY CHECKS ===' AS section;

-- Check for Spain-specific data
SELECT 'Spain Data Validation' AS check_type,
       'Customers in Spain regions' AS metric,
       COUNT(*) AS count
FROM PF_CUSTOMER_DIM
WHERE city IN ('Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Málaga', 'Zaragoza');

-- Check SF Accounts are Spain-based
SELECT 'SF Accounts Spain Check' AS check_type,
       SUM(CASE WHEN billing_state IN ('Comunidad de Madrid', 'Cataluña', 'Comunidad Valenciana', 'Andalucía', 'País Vasco', 'Aragón', 'Castilla y León', 'Galicia', 'Canarias', 'Región de Murcia') THEN 1 ELSE 0 END) AS spain_accounts,
       COUNT(*) AS total_accounts,
       ROUND(100.0 * SUM(CASE WHEN billing_state IN ('Comunidad de Madrid', 'Cataluña', 'Comunidad Valenciana', 'Andalucía', 'País Vasco', 'Aragón', 'Castilla y León', 'Galicia', 'Canarias', 'Región de Murcia') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_spain
FROM PF_SF_ACCOUNTS;

-- Check SF Contacts have Spain phone numbers
SELECT 'SF Contacts Spain Phone Check' AS check_type,
       SUM(CASE WHEN phone LIKE '+34%' THEN 1 ELSE 0 END) AS spain_phones,
       COUNT(*) AS total_contacts,
       ROUND(100.0 * SUM(CASE WHEN phone LIKE '+34%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_spain
FROM PF_SF_CONTACTS;

-- ========================================================================
-- SECTION 10: SUMMARY REPORT
-- ========================================================================

SELECT '=== VALIDATION SUMMARY ===' AS section;

WITH table_counts AS (
    SELECT 'Dimension Tables' AS category, 14 AS expected,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' 
            AND TABLE_NAME LIKE 'PF_%_DIM') AS actual
    UNION ALL
    SELECT 'Fact Tables', 4,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' 
            AND TABLE_NAME LIKE 'PF_%_FACT')
    UNION ALL
    SELECT 'Salesforce Tables', 3,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' 
            AND TABLE_NAME LIKE 'PF_SF_%')
    UNION ALL
    SELECT 'Parsed Content Tables', 3,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' 
            AND TABLE_NAME LIKE 'PF_PARSED_%')
    UNION ALL
    SELECT 'Semantic Views', 5,
           (SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = 'PREMIUMFIBER_SCHEMA' 
            AND TABLE_NAME LIKE 'PF_%_SEMANTIC_VIEW')
)
SELECT category,
       expected,
       actual,
       CASE WHEN actual >= expected THEN '✓ PASS' ELSE '✗ FAIL' END AS status
FROM table_counts;

-- Total row counts
SELECT 'Total Data Rows' AS metric,
       (SELECT COUNT(*) FROM PF_CUSTOMER_DIM) +
       (SELECT COUNT(*) FROM PF_SALES_FACT) +
       (SELECT COUNT(*) FROM PF_SF_ACCOUNTS) +
       (SELECT COUNT(*) FROM PF_SF_OPPORTUNITIES) +
       (SELECT COUNT(*) FROM PF_SF_CONTACTS) AS total_rows;

SELECT '=== VALIDATION COMPLETE ===' AS section;
