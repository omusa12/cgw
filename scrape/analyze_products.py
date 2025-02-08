import json
import os
from collections import defaultdict
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

def analyze_warranty_products(contracts):
    """Analyze warranty product details and pricing."""
    warranty_products = defaultdict(list)
    
    for contract in contracts:
        if contract.get('model_class') == 'App\\Contracts\\Warranty\\WarrantyContract':
            product = contract.get('product', {})
            if product:
                warranty_products['type'].append(product.get('type', ''))
                warranty_products['term'].append(product.get('term', ''))
                warranty_products['distance'].append(product.get('distance', ''))
                warranty_products['dealer_cost'].append(product.get('dealer_cost', 0))
                warranty_products['claim_amount'].append(product.get('claim_amount', 0))
                warranty_products['max_model_years'].append(product.get('max_model_years', 0))
                warranty_products['max_model_km'].append(product.get('max_model_km', 0))
    
    df = pd.DataFrame(warranty_products)
    
    print("\nWarranty Product Analysis")
    print("-" * 80)
    
    print("\nWarranty Types:")
    print(df['type'].value_counts().head(10))
    
    print("\nCommon Terms:")
    print(df['term'].value_counts().head(10))
    
    print("\nDistance Limits:")
    print(df['distance'].value_counts().head(10))
    
    print("\nPricing Analysis:")
    print(f"Average Dealer Cost: ${df['dealer_cost'].mean()/100:,.2f}")
    print(f"Max Dealer Cost: ${df['dealer_cost'].max()/100:,.2f}")
    print(f"Min Dealer Cost: ${df['dealer_cost'].min()/100:,.2f}")

def analyze_gap_products(contracts):
    """Analyze GAP insurance products."""
    gap_products = []
    
    for contract in contracts:
        if 'GAP' in contract.get('model_class', ''):
            product = contract.get('product', {})
            if product:
                try:
                    term_months = int(product.get('term_months', 0))
                except (ValueError, TypeError):
                    term_months = 0
                    
                gap_products.append({
                    'type': product.get('type', ''),
                    'term_months': term_months,
                    'dealer_cost': product.get('dealer_cost', 0),
                    'double_gap': bool(product.get('double_gap', False))
                })
    
    if gap_products:
        df = pd.DataFrame(gap_products)
        
        print("\nGAP Product Analysis")
        print("-" * 80)
        
        # Filter out 0 term months for the distribution
        valid_terms = df[df['term_months'] > 0]
        if not valid_terms.empty:
            print("\nTerm Length Distribution (months):")
            print(valid_terms['term_months'].value_counts().sort_index())
        
        print("\nPricing Analysis:")
        print(f"Average Dealer Cost: ${df['dealer_cost'].mean()/100:,.2f}")
        print(f"Double GAP Contracts: {df['double_gap'].sum()}")
        print(f"Total GAP Contracts: {len(df)}")

def analyze_vehicle_types(contracts):
    """Analyze vehicle types and their characteristics."""
    # Initialize the nested defaultdict with proper data structures
    vehicle_data = {}
    
    for contract in contracts:
        vehicle = contract.get('vehicle', {})
        if vehicle:
            make = vehicle.get('make', 'Unknown')
            model = vehicle.get('model', 'Unknown')
            year = vehicle.get('year', 0)
            usage = vehicle.get('vehicle_usage', 'Unknown')
            
            if make not in vehicle_data:
                vehicle_data[make] = {
                    'total': 0,
                    'models': set(),
                    'years': set(),
                    'usage_types': set()
                }
            
            vehicle_data[make]['total'] += 1
            vehicle_data[make]['models'].add(model)
            if year:
                vehicle_data[make]['years'].add(year)
            vehicle_data[make]['usage_types'].add(usage)
    
    print("\nVehicle Analysis")
    print("-" * 80)
    
    print("\nTop 10 Vehicle Makes:")
    sorted_makes = sorted(vehicle_data.items(), key=lambda x: x[1]['total'], reverse=True)
    for make, data in sorted_makes[:10]:
        print(f"\n{make}:")
        print(f"Total Contracts: {data['total']}")
        print(f"Unique Models: {len(data['models'])}")
        if data['years']:
            print(f"Year Range: {min(data['years'])} - {max(data['years'])}")
        print(f"Usage Types: {', '.join(data['usage_types'])}")

def main():
    print("Loading contract data...")
    contracts = load_json_files('scraped_data')
    
    analyze_warranty_products(contracts)
    analyze_gap_products(contracts)
    analyze_vehicle_types(contracts)

if __name__ == "__main__":
    main()
