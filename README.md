# QC Laboratory Data Automation and Integrity

This repository contains technical scripts developed for data validation, Master Data specification mapping, and OOS (Out-of-Specification) tracking within GxP and FDA regulated pharmaceutical environments.

The project demonstrates the application of Python and SQL to streamline data workflows between analytical instruments (e.g., Empower) and laboratory informatics platforms (LIMS).

## Repository Structure

* lab_data_processor.py: Python script utilizing pandas for raw instrument data ingestion, parsing, and automated OOS alert triggers.
* lims_database_queries.sql: SQL schema and analytical audit queries designed to match standard LIMS data structures.

## Technical Details

### Python Data Validation
The script processes automated JSON outputs from laboratory middleware, handles missing values, and checks dynamic analytical results against master product criteria.
* Core libraries: pandas, numpy, json.
* Key logic: Automated calculation of product variables and conditional flag handling.

### SQL LIMS Schemas
A relational database layout representing standard Master Data tables and transactional sample tracking.
* Tables included: master_data_specs, sample_results.
* Compliance Query: Utilizes conditional logic to auto-audit laboratory entries and output status flags (PASS / OOS_ALERT) for data integrity verification.

## Usage

Ensure you have python 3.x and pandas installed before execution:

pip install pandas numpy
python lab_data_processor.py
