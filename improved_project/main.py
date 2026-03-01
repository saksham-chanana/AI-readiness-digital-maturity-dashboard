import argparse
import os
from src.generator import generate_dummy_data
from src.processor import process_data
from src.analytics import extract_insights, generate_visualizations

def main():
    parser = argparse.ArgumentParser(description="Survey Project Pipeline Orchestrator")
    parser.add_argument("--samples", type=int, default=200, help="Number of dummy samples to generate")
    parser.add_argument("--output-dir", type=str, default="data", help="Directory to save generated CSV files")
    parser.add_argument("--charts-dir", type=str, default="output", help="Directory to save generated visualizations")
    
    args = parser.parse_args()
    
    # Define file paths
    raw_data_path = os.path.join(args.output_dir, "dummy_responses.csv")
    processed_data_path = os.path.join(args.output_dir, "processed_responses.csv")
    
    print("\n--- PHASE 1: DATA GENERATION ---")
    df_raw = generate_dummy_data(num_samples=args.samples, output_path=raw_data_path)
    print(f"Generated {args.samples} records.")
    
    print("\n--- PHASE 2: DATA PROCESSING ---")
    df_processed = process_data(df_raw, output_path=processed_data_path)
    
    print("\n--- PHASE 3: INSIGHT EXTRACTION ---")
    insights_tuple = extract_insights(df_processed)
    insights_dict = insights_tuple[0]
    
    print(f"Extracted insights for Tool Adoption: {insights_dict['tool_adoption']['cloud']} Cloud vs {insights_dict['tool_adoption']['traditional']} Traditional")
    print(f"Identified {insights_dict['silo_effect']['inconsistent_data']} businesses with siloed and inconsistent data")
    print(f"Found a gap of {insights_dict['ai_gap']['gap']} businesses who want AI but aren't actively using it")
    print(f"Found {insights_dict['manufacturing']['bottleneck']} manufacturing businesses with automation bottlenecks")
    
    print("\n--- PHASE 4: VISUALIZATION ---")
    generate_visualizations(df_processed, insights_tuple, output_dir=args.charts_dir)
    print("\nPipeline Complete!")

if __name__ == "__main__":
    main()
