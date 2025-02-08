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

def analyze_contract_types(contracts):
    """Analyze contract types and their relationships."""
    
    # Create mappings for analysis
    model_class_to_type = defaultdict(set)
    type_to_product = defaultdict(set)
    model_class_counts = defaultdict(int)
    contract_type_counts = defaultdict(int)
    
    # Analyze relationships
    for contract in contracts:
        model_class = contract.get('model_class', '')
        contract_type = contract.get('contract_type', '')
        product_info = contract.get('product', {})
        
        model_class_counts[model_class] += 1
        contract_type_counts[contract_type] += 1
        model_class_to_type[model_class].add(contract_type)
        
        if product_info:
            product_type = product_info.get('type', '')
            if product_type:
                type_to_product[contract_type].add(product_type)
    
    # Print analysis
    print("\nContract Type Analysis")
    print("-" * 80)
    
    print("\nModel Classes:")
    for model_class, count in model_class_counts.items():
        print(f"\n{model_class}:")
        print(f"Count: {count}")
        print(f"Associated contract types: {', '.join(model_class_to_type[model_class])}")
    
    print("\nContract Types:")
    for contract_type, count in contract_type_counts.items():
        print(f"\n{contract_type}:")
        print(f"Count: {count}")
        if type_to_product[contract_type]:
            print(f"Associated product types: {', '.join(type_to_product[contract_type])}")
    
    # Analyze product details by contract type
    print("\nDetailed Product Analysis by Contract Type")
    print("-" * 80)
    
    for contract in contracts[:1000]:  # Analyze first 1000 for sample
        if contract.get('product'):
            contract_type = contract.get('contract_type', '')
            product = contract.get('product', {})
            print(f"\nContract Type: {contract_type}")
            print("Product Details:")
            for key, value in product.items():
                print(f"  {key}: {value}")
            print("-" * 40)
            break  # Show one example per contract type

def main():
    print("Loading contract data...")
    contracts = load_json_files('scraped_data')
    
    print("\nAnalyzing contract types...")
    analyze_contract_types(contracts)

if __name__ == "__main__":
    main()
