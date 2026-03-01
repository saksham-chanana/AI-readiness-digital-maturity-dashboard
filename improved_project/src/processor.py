import pandas as pd
import os

def calculate_maturity(row):
    # Base score out of 30, scaled to 100
    score = 0
    
    # 1. Cloud & Integration (Max: 10 points)
    if row["Q6_Internal_Operations"] == "Digitally (using Software/Tools)":
        score += 2
        
    cloud_status = row.get("Q6.2_Cloud_Deployment", "")
    if cloud_status in ["Cloud based Software systems", "Fully managed by software vendors/service providers"]:
        score += 4
    elif cloud_status == "Partly On-Premises /Cloud Based":
        score += 2
            
    integration = row.get("Q6.3_Integration", "")
    if integration == "Fully integrated":
        score += 4
    elif integration == "Partially integrated":
        score += 2
        
    # 2. Data Management & Security (Max: 10 points)
    doc_mgmt = row.get("Q7_Document_Management", "")
    if doc_mgmt == "Document management system (DMS)":
        score += 3
    elif doc_mgmt == "Cloud Storage":
        score += 2
        
    data_consist = row.get("Q10_Data_Consistency", "")
    if data_consist == "Yes":
        score += 2
        
    data_qual = row.get("Q13_Data_Quality", "")
    if data_qual in ["Automated checks", "Data quality is continuously monitored"]:
        score += 2
        
    data_sec = row.get("Q14_Data_Security", "")
    if data_sec in ["Advanced security with regular assessments", "Defined security policies and controls"]:
        score += 3
    elif data_sec == "Basic security measures in place":
        score += 1
        
    # 3. AI & Analytics Capability (Max: 10 points)
    ai_usage = row.get("Q15_AI_Usage", "")
    if ai_usage in ["Yes, AI is actively used across multiple business functions", "AI is central to our core decision-making"]:
        score += 6
    elif ai_usage == "We use AI in a few specific or pilot use cases":
        score += 2
    elif ai_usage == "We are exploring or learning about AI":
        score += 1
        
    ai_invest = row.get("Q18_AI_Investment", "")
    if ai_invest == "Yes":
        score += 2
    elif ai_invest == "Maybe":
        score += 1
        
    hist_data = row.get("Q9_Historical_Data", "")
    if hist_data == "Yes":
        score += 2
        
    # Scale to 100
    final_score = (score / 30.0) * 100
    return round(final_score, 1)


def categorize_maturity(score):
    if score < 34:
        return "Digital Laggard"
    elif score < 67:
        return "Digital Adopter"
    else:
        return "Digital Leader"

def process_data(df, output_path=None):
    """
    Process the Data: Apply Weighted Scoring and Maturity Categories
    """
    processed_df = df.copy()
    
    # Calculate score row by row
    scores = []
    for _, row in processed_df.iterrows():
        scores.append(calculate_maturity(row))
        
    processed_df["Maturity_Score"] = scores
    processed_df["Maturity_Category"] = processed_df["Maturity_Score"].apply(categorize_maturity)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        processed_df.to_csv(output_path, index=False)
        print(f"Successfully processed data -> {output_path}")
        
    return processed_df

if __name__ == "__main__":
    if os.path.exists("../data/dummy_responses.csv"):
        df = pd.read_csv("../data/dummy_responses.csv")
        process_data(df, output_path="../data/processed_responses.csv")
