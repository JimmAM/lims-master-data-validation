-- =====================================================================
-- LIMS SCHEMA & QUALITY CONTROL AUDIT QUERIES
-- Purpose: Simulating Master Data structures and OOS monitoring.
-- =====================================================================

-- 1. Create Master Data Specifications Table
CREATE TABLE master_data_specs (
    spec_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    min_limit DECIMAL(10, 2),
    max_limit DECIMAL(10, 2),
    unit VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Sample Test Results Table (Transactional Data)
CREATE TABLE sample_results (
    sample_id VARCHAR(50) PRIMARY KEY,
    spec_id VARCHAR(50),
    measured_value DECIMAL(10, 2),
    analyst_name VARCHAR(100),
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (spec_id) REFERENCES master_data_specs(spec_id)
);

-- 3. Insert Dummy Master Data (GxP Compliant structures)
INSERT INTO master_data_specs (spec_id, product_name, min_limit, max_limit, unit) VALUES
('SPEC-ACET-99', 'Acetaminophen 99%', 98.00, 102.00, '%'),
('SPEC-IBU-400', 'Ibuprofen 400mg', 380.00, 420.00, 'mg');

INSERT INTO sample_results (sample_id, spec_id, measured_value, analyst_name) VALUES
('SMP-2026-001', 'SPEC-ACET-99', 99.50, 'John Doe'),
('SMP-2026-002', 'SPEC-ACET-99', 97.20, 'Jane Smith'), -- OOS Sample
('SMP-2026-003', 'SPEC-IBU-400', 415.00, 'John Doe');

-- =====================================================================
-- AUDIT & COMPLIANCE QUERY: Automated OOS & Data Integrity Detection
-- =====================================================================
-- This query automatically calculates compliance status by joining 
-- analytical results with hardcoded Master Data specifications.

SELECT 
    r.sample_id,
    m.product_name,
    r.measured_value,
    m.min_limit,
    m.max_limit,
    m.unit,
    r.analyst_name,
    r.analysis_date,
    CASE 
        WHEN r.measured_value BETWEEN m.min_limit AND m.max_limit THEN 'PASS'
        ELSE 'OOS_ALERT'
    END AS quality_status
FROM 
    sample_results r
INNER JOIN 
    master_data_specs m ON r.spec_id = m.spec_id
ORDER BY 
    r.analysis_date DESC;
