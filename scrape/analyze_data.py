import json
import os
from collections import defaultdict
from datetime import datetime
import pandas as pd

def load_json_files(directory):
    """Load all JSON files from the specified directory."""
    all_contracts = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r') as f:
                    contracts = json.load(f)
                    if isinstance(contracts, list):
                        all_contracts.extend(contracts)
                    else:
                        all_contracts.append(contracts)
            except json.JSONDecodeError:
                print(f"Error reading {filename}")
    return all_contracts

def analyze_data_structure(contracts):
    """Analyze the structure of the data and print field information."""
    if not contracts:
        print("No contracts found")
        return

    # Analyze fields
    field_counts = defaultdict(int)
    field_types = defaultdict(set)
    sample_values = defaultdict(set)
    
    for contract in contracts[:1000]:  # Analyze first 1000 contracts
        for field, value in contract.items():
            field_counts[field] += 1
            field_types[field].add(type(value).__name__)
            if value is not None:
                # Store a few sample values for each field
                if len(sample_values[field]) < 3:
                    sample_values[field].add(str(value))

    # Print analysis
    print("\nField Analysis:")
    print("-" * 80)
    print(f"Total number of contracts analyzed: {len(contracts)}")
    print("-" * 80)
    
    for field in field_counts.keys():
        print(f"\nField: {field}")
        print(f"Occurrence: {field_counts[field]} times")
        print(f"Data types: {', '.join(field_types[field])}")
        print(f"Sample values: {', '.join(list(sample_values[field]))}")

def generate_basic_stats(contracts):
    """Generate basic statistics about the contracts."""
    if not contracts:
        return

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(contracts)
    
    print("\nBasic Statistics:")
    print("-" * 80)
    
    # Time range analysis
    if 'contract_date' in df.columns:
        df['contract_date'] = pd.to_datetime(df['contract_date'])
        print(f"\nDate Range:")
        print(f"Earliest contract: {df['contract_date'].min()}")
        print(f"Latest contract: {df['contract_date'].max()}")
        
        # Contracts per year
        print("\nContracts per year:")
        print(df['contract_date'].dt.year.value_counts().sort_index())

    # Count unique values for categorical fields
    categorical_fields = ['warranty_type', 'vehicle_make', 'vehicle_model']
    for field in categorical_fields:
        if field in df.columns:
            print(f"\nTop 10 {field}:")
            print(df[field].value_counts().head(10))

def main():
    directory = 'scraped_data'
    print("Loading contract data...")
    contracts = load_json_files(directory)
    
    print("\nAnalyzing data structure...")
    analyze_data_structure(contracts)
    
    print("\nGenerating basic statistics...")
    generate_basic_stats(contracts)

if __name__ == "__main__":
    main()
