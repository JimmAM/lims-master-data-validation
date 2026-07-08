import pandas as pd
import numpy as np
import json

# Simulation of Master Data specifications (hardcoded, as implemented in the system)
MASTER_DATA_SPECS = {
    "Acetaminophen_99": {"min_limit": 98.0, "max_limit": 102.0, "unit": "%"},
    "Ibuprofen_400": {"min_limit": 380.0, "max_limit": 420.0, "unit": "mg"},
}

def load_raw_lab_data(json_payload):
    """Simulates the receipt of a JSON payload from an instrument's middleware."""
    try:
        data = json.loads(json_payload)
        return pd.DataFrame(data)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse instrument data payload: {e}")
        return None

def validate_specifications(df, specs):
    """
    Processes the variables, executes the analytical calculation, and maps
    against strict Master Data limits (OOS detection).
    """
    if df is None or df.empty:
        return None
    
    # Basic data cleaning (removing nulls in critical measurements)
    df = df.dropna(subset=['measured_value'])
    
    validated_records = []
    
    for index, row in df.iterrows():
        product = row['product_id']
        measured = float(row['measured_value'])
        
        if product in specs:
            min_lim = specs[product]['min_limit']
            max_lim = specs[product]['max_limit']
            
            # Logical evaluation of specification
            is_oos = not (min_lim <= measured <= max_lim)
            status = "OOS" if is_oos else "PASS"
        else:
            status = "UNKNOWN_PRODUCT"
            is_oos = True
            
        record = {
            "sample_id": row['sample_id'],
            "product_id": product,
            "measured_value": measured,
            "status": status,
            "oos_flag": is_oos
        }
        validated_records.append(record)
        
    return pd.DataFrame(validated_records)

if __name__ == "__main__":
    # Test payload: Simulates raw data with a read error and an actual OOS.
    raw_instrument_output = """
    [
        {"sample_id": "SMP-001", "product_id": "Acetaminophen_99", "measured_value": 99.5},
        {"sample_id": "SMP-002", "product_id": "Acetaminophen_99", "measured_value": 97.2},
        {"sample_id": "SMP-003", "product_id": "Ibuprofen_400", "measured_value": 415.0},
        {"sample_id": "SMP-004", "product_id": "Ibuprofen_400", "measured_value": null}
    ]
    """
    
    print("--- Starting Automated Lab Data Ingestion ---")
    df_raw = load_raw_lab_data(raw_instrument_output)
    
    print("\n--- Running Master Data Specification Validation ---")
    df_validated = validate_specifications(df_raw, MASTER_DATA_SPECS)
    
    print("\n[RESULT] Processed Laboratory Data:")
    print(df_validated.to_string(index=False))
    
    # Automatic alert if OOS is detected.
    if df_validated['oos_flag'].any():
        print("\n[ALERT] Out of Specification (OOS) detected! Triggering quality review protocol.")
