import pandas as pd
import numpy as np
import random

def generate_dummy_data(num_samples=200):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for _ in range(num_samples):
        # Determine Persona
        rand_val = random.random()
        if rand_val < 0.4:
            persona = "Traditionalist"
        elif rand_val < 0.8:
            persona = "Transitioning MSME"
        else:
            persona = "Tech-Savvy Digital Native"
            
        row = {"Persona": persona}
        
        # Q1: Customer Discovery & Options
        if persona == "Traditionalist":
            row["Q1_Customer_Discovery"] = "Manual / Partially Digital"
            row["Q1.1_Manual_Methods"] = random.choice(["Word of mouth only", "Social Media (WhatsApp, Facebook, Instagram)"])
            row["Q1.2_Retail_Marketplaces"] = "N/A"
            row["Q1.3_Digital_Trade"] = "N/A"
            row["Q1.4_Quick_Commerce"] = "N/A"
            row["Q1.5_Gov_Portals"] = "N/A"
        elif persona == "Transitioning MSME":
            row["Q1_Customer_Discovery"] = random.choice(["Online Retail Marketplaces", "Digital Trade Platforms"])
            if row["Q1_Customer_Discovery"] == "Online Retail Marketplaces":
                row["Q1.2_Retail_Marketplaces"] = random.choice(["Amazon", "Flipkart", "Meesho", "Amazon, Flipkart"])
                row["Q1.3_Digital_Trade"] = "N/A"
            else:
                row["Q1.2_Retail_Marketplaces"] = "N/A"
                row["Q1.3_Digital_Trade"] = random.choice(["IndiaMART", "TradeIndia", "IndiaMART, TradeIndia"])
            row["Q1.1_Manual_Methods"] = "N/A"
            row["Q1.4_Quick_Commerce"] = "N/A"
            row["Q1.5_Gov_Portals"] = "N/A"
        else:
            row["Q1_Customer_Discovery"] = random.choice(["Online Retail Marketplaces", "Digital Trade Platforms", "Quick Commerce Platforms", "Government Portals"])
            row["Q1.1_Manual_Methods"] = "N/A"
            row["Q1.2_Retail_Marketplaces"] = random.choice(["Amazon, Flipkart", "N/A"]) if row["Q1_Customer_Discovery"] != "Online Retail Marketplaces" else random.choice(["Amazon", "Flipkart", "Amazon, Flipkart"])
            row["Q1.3_Digital_Trade"] = random.choice(["IndiaMART, TradeIndia", "N/A"]) if row["Q1_Customer_Discovery"] != "Digital Trade Platforms" else random.choice(["IndiaMART", "TradeIndia", "IndiaMART, TradeIndia"])
            row["Q1.4_Quick_Commerce"] = random.choice(["Blinkit, Swiggy Instamart", "Zepto", "N/A"]) if row["Q1_Customer_Discovery"] == "Quick Commerce Platforms" else "N/A"
            row["Q1.5_Gov_Portals"] = random.choice(["Udyam Portal", "GeM – Government e-Marketplace", "N/A"]) if row["Q1_Customer_Discovery"] == "Government Portals" else "N/A"

        # Q2 & Q2.2: Customer Communication
        if persona == "Traditionalist":
            row["Q2_Communication"] = random.choice(["Manually (Phone calls/In-person)", "Messaging Tools (SMS/Email/WhatsApp/Social Media)"])
            row["Q2.2_CRM_Software"] = "N/A"
        elif persona == "Transitioning MSME":
            row["Q2_Communication"] = random.choice(["Messaging Tools (SMS/Email/WhatsApp/Social Media)", "Basic Customer Software (Standard or Custom made)"])
            row["Q2.2_CRM_Software"] = "N/A"
        else:
            row["Q2_Communication"] = "Advanced Digital Software / CRM Software"
            row["Q2.2_CRM_Software"] = random.choice(["Zoho CRM", "Salesforce Essentials", "HubSpot CRM", "Freshworks CRM", "Zoho CRM, HubSpot CRM"])

        # Q3 & Q3.1: Feedback
        if persona == "Traditionalist":
            row["Q3_Feedback"] = random.choice(["No formal recording (Verbal only)", "Recorded manually in a diary or register"])
            row["Q3.1_Ticketing_Tool"] = "N/A"
        elif persona == "Transitioning MSME":
            row["Q3_Feedback"] = random.choice(["Recorded manually in a diary or register", "Recorded in Excel/Spreadsheets"])
            row["Q3.1_Ticketing_Tool"] = "N/A"
        else:
            row["Q3_Feedback"] = "Managed through a digital ticketing system or CRM"
            row["Q3.1_Ticketing_Tool"] = random.choice(["Freshdesk", "Zendesk", "Zoho Desk", "Salesforce Service Cloud", "Zendesk, Zoho Desk"])

        # Q4 & Q4.1: Repeat Customers
        if persona == "Traditionalist":
            row["Q4_Repeat_Customers"] = "We do not track repeat customers digitally"
            row["Q4.1_Repeat_Tracking_Tool"] = "N/A"
        elif persona == "Transitioning MSME":
            row["Q4_Repeat_Customers"] = "We track repeat customers manually using basic digital tools"
            row["Q4.1_Repeat_Tracking_Tool"] = "N/A"
        else:
            row["Q4_Repeat_Customers"] = "We track repeat customers through advanced digital tools"
            row["Q4.1_Repeat_Tracking_Tool"] = random.choice(["Zoho CRM", "HubSpot CRM", "Freshsales", "TallyPrime", "Zoho CRM, Freshsales"])

        # Q5 & Q5.1: Drop-offs
        if persona == "Traditionalist":
            row["Q5_Drop_offs"] = "We do not track customer drop-offs"
            row["Q5.1_Drop_off_Tool"] = "N/A"
        elif persona == "Transitioning MSME":
            row["Q5_Drop_offs"] = random.choice(["We do not track customer drop-offs", "We track customer drop-offs informally or manually"])
            row["Q5.1_Drop_off_Tool"] = "N/A"
        else:
            row["Q5_Drop_offs"] = "We track customer drop-offs using basic/advanced digital tools"
            row["Q5.1_Drop_off_Tool"] = random.choice(["Abandoned carts", "Bounce/drop-off pages", "Zoho CRM", "HubSpot CRM", "CleverTap", "Mailchimp", "Abandoned carts, HubSpot CRM"])

        # Q6 - Core Operations
        if persona == "Traditionalist":
            row["Q6_Internal_Operations"] = "Manually"
            row["Q6.1_Digital_Areas"] = "N/A"
            row["Q6.1.1_Productivity_Tools"] = "N/A"
            row["Q6.1.2_Sales_Marketing_Tools"] = "N/A"
            row["Q6.1.3_Operations_Tools"] = "N/A"
            row["Q6.1.4_Inventory_Tools"] = "N/A"
            row["Q6.1.5_Manufacturing_Tools"] = "N/A"
            row["Q6.1.6_Supply_Chain_Tools"] = "N/A"
            row["Q6.1.8_Accounting_Tools"] = "N/A"
            row["Q6.1.9_Analytics_Tools"] = "N/A"
            row["Q6.2_Cloud_Deployment"] = "N/A"
            row["Q6.2.1_Cloud_Details"] = "N/A"
            row["Q6.3_Integration"] = "Not integrated"
        else:
            row["Q6_Internal_Operations"] = "Digitally (using Software/Tools)"
            
            if persona == "Transitioning MSME":
                areas = random.sample(["General Productivity & Office Work", "Sales & Marketing", "Inventory Management", "Accounting & Finance"], k=random.randint(1, 3))
                row["Q6.1_Digital_Areas"] = ", ".join(areas)
                row["Q6.1.1_Productivity_Tools"] = random.choice(["Zoho Workplace", "Trello", "Slack", "N/A"]) if "General Productivity & Office Work" in areas else "N/A"
                row["Q6.1.2_Sales_Marketing_Tools"] = random.choice(["Interakt", "WATI", "N/A"]) if "Sales & Marketing" in areas else "N/A"
                row["Q6.1.3_Operations_Tools"] = "N/A"
                row["Q6.1.4_Inventory_Tools"] = random.choice(["myBillBook", "Vyapar Inventory", "N/A"]) if "Inventory Management" in areas else "N/A"
                row["Q6.1.5_Manufacturing_Tools"] = "N/A"
                row["Q6.1.6_Supply_Chain_Tools"] = "N/A"
                row["Q6.1.8_Accounting_Tools"] = random.choice(["Tally Prime", "Zoho Books", "Vyapar"]) if "Accounting & Finance" in areas else "N/A"
                row["Q6.1.9_Analytics_Tools"] = "N/A"
                
                row["Q6.2_Cloud_Deployment"] = random.choice(["On Premises Software Systems", "Cloud based Software systems", "Partly On-Premises /Cloud Based"])
                row["Q6.2.1_Cloud_Details"] = random.choice(["AWS (Amazon Web Services)", "Zoho Cloud", "N/A"]) if "Cloud" in row["Q6.2_Cloud_Deployment"] else "N/A"
                row["Q6.3_Integration"] = random.choice(["Not integrated", "Partially integrated"])
                
            else: # Tech-Savvy
                areas = random.sample(["General Productivity & Office Work", "Sales & Marketing", "Operations & Process Management", "Inventory Management", "Manufacturing & Production", "Supply Chain & Procurement", "Accounting & Finance", "Data, Reporting & Analytics"], k=random.randint(4, 7))
                row["Q6.1_Digital_Areas"] = ", ".join(areas)
                row["Q6.1.1_Productivity_Tools"] = random.choice(["Zoho Workplace, Slack", "Asana, Notion", "Trello, Slack"]) if "General Productivity & Office Work" in areas else "N/A"
                row["Q6.1.2_Sales_Marketing_Tools"] = random.choice(["HubSpot", "Freshsales", "LeadSquared"]) if "Sales & Marketing" in areas else "N/A"
                row["Q6.1.3_Operations_Tools"] = random.choice(["ERPNext", "Zoho One", "Microsoft Power Automate"]) if "Operations & Process Management" in areas else "N/A"
                row["Q6.1.4_Inventory_Tools"] = random.choice(["Zoho Inventory", "ERPNext"]) if "Inventory Management" in areas else "N/A"
                row["Q6.1.5_Manufacturing_Tools"] = random.choice(["ERPNext", "Zoho ERP for Manufacturing"]) if "Manufacturing & Production" in areas else "N/A"
                row["Q6.1.6_Supply_Chain_Tools"] = random.choice(["ERPNext", "Locus", "Zoho Inventory"]) if "Supply Chain & Procurement" in areas else "N/A"
                row["Q6.1.8_Accounting_Tools"] = random.choice(["Zoho Books", "Tally Prime"]) if "Accounting & Finance" in areas else "N/A"
                row["Q6.1.9_Analytics_Tools"] = random.choice(["Zoho Analytics", "Microsoft Power BI", "Google Looker Studio"]) if "Data, Reporting & Analytics" in areas else "N/A"
                
                row["Q6.2_Cloud_Deployment"] = random.choice(["Cloud based Software systems", "Fully managed by software vendors/service providers"])
                row["Q6.2.1_Cloud_Details"] = random.choice(["AWS (Amazon Web Services)", "Microsoft Azure", "Google Cloud Platform (GCP)"])
                row["Q6.3_Integration"] = random.choice(["Partially integrated", "Fully integrated"])

        # Q7-Q10: Data Management
        if persona == "Traditionalist":
            row["Q7_Document_Management"] = "Digital files on local devices"
            row["Q8_Backup_Frequency"] = random.choice(["Never", "Occasionally (Only When Someone Remembers)"])
            row["Q9_Historical_Data"] = "No"
            row["Q10_Data_Consistency"] = "No"
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing"])
        elif persona == "Transitioning MSME":
            row["Q7_Document_Management"] = random.choice(["Digital files on local devices", "Cloud Storage"])
            row["Q8_Backup_Frequency"] = random.choice(["Occasionally (Only When Someone Remembers)", "Regularly (Weekly or Monthly)"])
            row["Q9_Historical_Data"] = random.choice(["Yes", "No"])
            row["Q10_Data_Consistency"] = random.choice(["Yes", "No"])
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing", "IT"])
        else:
            row["Q7_Document_Management"] = random.choice(["Cloud Storage", "Document management system (DMS)"])
            row["Q8_Backup_Frequency"] = random.choice(["Regularly (Weekly or Monthly)", "Automatically (Daily or Real-time)"])
            row["Q9_Historical_Data"] = "Yes"
            row["Q10_Data_Consistency"] = "Yes"
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing", "IT", "Finance"])

        # Q11-Q12: Manufacturing Specific
        if row["Industry"] == "Manufacturing":
            if persona == "Traditionalist":
                row["Q11_Manufacturing_Automated"] = "No"
                row["Q12_Machines_Integrated"] = "No"
            elif persona == "Transitioning MSME":
                row["Q11_Manufacturing_Automated"] = random.choice(["Yes", "No"])
                row["Q12_Machines_Integrated"] = random.choice(["Yes", "No"]) if row["Q11_Manufacturing_Automated"] == "Yes" else "No"
            else:
                row["Q11_Manufacturing_Automated"] = "Yes"
                row["Q12_Machines_Integrated"] = random.choice(["Yes", "Not Applicable"])
        else:
            row["Q11_Manufacturing_Automated"] = "Not Applicable"
            row["Q12_Machines_Integrated"] = "Not Applicable"

        # Q13-Q14: Data Quality & Security
        if persona == "Traditionalist":
            row["Q13_Data_Quality"] = "No defined process for data accuracy"
            row["Q14_Data_Security"] = random.choice(["Minimal / ad-hoc", "Basic security measures in place"])
        elif persona == "Transitioning MSME":
            row["Q13_Data_Quality"] = random.choice(["Basic checks done manually", "Regular reviews or validations"])
            row["Q14_Data_Security"] = random.choice(["Basic security measures in place", "Defined security policies and controls"])
        else:
            row["Q13_Data_Quality"] = random.choice(["Automated checks", "Data quality is continuously monitored"])
            row["Q14_Data_Security"] = random.choice(["Defined security policies and controls", "Advanced security with regular assessments"])

        # Q15-Q18: AI Capability
        if persona == "Traditionalist":
            row["Q15_AI_Usage"] = "No, we do not currently use AI"
            row["Q15.1.1_AI_Productivity"] = "N/A"
            row["Q15.1.9_AI_Accounting"] = "N/A"
            row["Q16_AI_Training"] = "No guidelines"
            row["Q17_AI_Roadmap"] = "No roadmap"
            row["Q18_AI_Investment"] = random.choice(["No", "Maybe"])
        elif persona == "Transitioning MSME":
            row["Q15_AI_Usage"] = random.choice(["No, we do not currently use AI", "We are exploring or learning about AI", "We use AI in a few specific or pilot use cases"])
            if row["Q15_AI_Usage"] in ["We are exploring or learning about AI", "We use AI in a few specific or pilot use cases"]:
                row["Q15.1.1_AI_Productivity"] = random.choice(["ChatGPT", "Gemini", "N/A"])
                row["Q15.1.9_AI_Accounting"] = random.choice(["ChatGPT", "Tally Prime", "N/A"])
            else:
                row["Q15.1.1_AI_Productivity"] = "N/A"
                row["Q15.1.9_AI_Accounting"] = "N/A"
            row["Q16_AI_Training"] = random.choice(["No guidelines", "Informal guidance"])
            row["Q17_AI_Roadmap"] = random.choice(["No roadmap", "Informal plans"])
            row["Q18_AI_Investment"] = random.choice(["Yes", "Maybe"])
        else:
            row["Q15_AI_Usage"] = random.choice(["We use AI in a few specific or pilot use cases", "AI is central to our core decision-making", "Yes, AI is actively used across multiple business functions"])
            row["Q15.1.1_AI_Productivity"] = random.choice(["ChatGPT, Notion AI", "Gemini, Workspace", "Copilot", "Zoom AI"])
            row["Q15.1.9_AI_Accounting"] = random.choice(["Power BI", "Zoho Analytics", "Tableau"])
            row["Q16_AI_Training"] = random.choice(["Documented policies", "SOPs Training and awareness programs"])
            row["Q17_AI_Roadmap"] = random.choice(["Defined roadmap", "Actively executing roadmap"])
            row["Q18_AI_Investment"] = "Yes"

        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_csv('/Users/sakshamchanana/Desktop/survey/dummy_responses.csv', index=False)
    print("Successfully generated dummy data -> dummy_responses.csv")
    return df

def process_data(df):
    """
    Process the Data: Handle Multi-selects and Generate Digital Maturity Score
    """
    
    def calculate_maturity(row):
        score = 0
        # Q6 - Operations
        if row["Q6_Internal_Operations"] == "Digitally (using Software/Tools)":
            score += 1
            if row["Q6.2_Cloud_Deployment"] in ["Cloud based Software systems", "Fully managed by software vendors/service providers"]:
                score += 3
            elif row["Q6.2_Cloud_Deployment"] == "Partly On-Premises /Cloud Based":
                score += 2
                
        if row["Q6.3_Integration"] == "Fully integrated":
            score += 4
        elif row["Q6.3_Integration"] == "Partially integrated":
            score += 2
            
        # Q7 - Document Management
        if row["Q7_Document_Management"] == "Document management system (DMS)":
            score += 3
        elif row["Q7_Document_Management"] == "Cloud Storage":
            score += 2
            
        # Q10 Data Consistency
        if row["Q10_Data_Consistency"] == "Yes":
            score += 2
            
        # Q13 & Q14 Security
        if row["Q13_Data_Quality"] in ["Automated checks", "Data quality is continuously monitored"]:
            score += 3
        if row["Q14_Data_Security"] in ["Advanced security with regular assessments", "Defined security policies and controls"]:
            score += 3
            
        # Q15 AI Usage
        if row["Q15_AI_Usage"] in ["Yes, AI is actively used across multiple business functions", "AI is central to our core decision-making"]:
            score += 5
        elif row["Q15_AI_Usage"] == "We use AI in a few specific or pilot use cases":
            score += 3
        elif row["Q15_AI_Usage"] == "We are exploring or learning about AI":
            score += 1
            
        return score
        
    df["Maturity_Score"] = df.apply(calculate_maturity, axis=1)
    
    df.to_csv('/Users/sakshamchanana/Desktop/survey/processed_responses.csv', index=False)
    print("Successfully processed data -> processed_responses.csv")
    return df

def extract_insights(df):
    print("\n--- PHASE 3: INSIGHT EXTRACTION ---\n")
    
    # 1. Tool Adoption & Market Penetration
    print("1. Tool Adoption (Traditional vs Cloud B2B for MSMEs)")
    msme_df = df[df['Persona'] == 'Transitioning MSME']
    traditional_accounting = msme_df[msme_df['Q6.1.8_Accounting_Tools'] == 'Tally Prime'].shape[0]
    cloud_accounting = msme_df[msme_df['Q6.1.8_Accounting_Tools'].isin(['Zoho Books', 'Vyapar'])].shape[0]
    total_msme = msme_df.shape[0]
    print(f"   Traditional Accounting (Tally Prime): {traditional_accounting} ({traditional_accounting/total_msme*100:.1f}%)")
    print(f"   Cloud Accounting (Zoho, Vyapar): {cloud_accounting} ({cloud_accounting/total_msme*100:.1f}%)")
    
    # 2. The "Silo" Effect
    print("\n2. The 'Silo' Effect (System Integration vs Data Consistency)")
    # Using multiple tools but lack integration -> manual data entry impact
    multiple_tools = df[df['Q6_Internal_Operations'] == 'Digitally (using Software/Tools)']
    siloed_businesses = multiple_tools[(multiple_tools['Q6.3_Integration'] == 'Not integrated') | (multiple_tools['Q6.3_Integration'] == 'Partially integrated')]
    inconsistent_data_in_silos = siloed_businesses[siloed_businesses['Q10_Data_Consistency'] == 'No'].shape[0]
    print(f"   Businesses using digital tools but not fully integrated: {siloed_businesses.shape[0]}")
    if siloed_businesses.shape[0] > 0:
        print(f"   Percentage of siloed businesses suffering from inconsistent data: {inconsistent_data_in_silos / siloed_businesses.shape[0] * 100:.1f}%")

    # 3. AI Readiness vs Reality
    print("\n3. AI Readiness vs Reality: Future Investment vs Current Usage")
    desire_to_invest = df[df['Q18_AI_Investment'] == 'Yes']
    actual_ai_usage = df[df['Q15_AI_Usage'].isin(['Yes, AI is actively used across multiple business functions', 'AI is central to our core decision-making'])]
    # Gap = those who want to invest but aren't heavily using it yet
    gap = desire_to_invest[~desire_to_invest['Q15_AI_Usage'].isin(['Yes, AI is actively used across multiple business functions', 'AI is central to our core decision-making'])]
    print(f"   Businesses planning to invest in AI: {desire_to_invest.shape[0]} ({desire_to_invest.shape[0]/df.shape[0]*100:.1f}%)")
    print(f"   Businesses currently using advanced AI: {actual_ai_usage.shape[0]} ({actual_ai_usage.shape[0]/df.shape[0]*100:.1f}%)")
    print(f"   Gap (Desire to invest vs Actual Advanced Use): {gap.shape[0]} ({gap.shape[0]/df.shape[0]*100:.1f}%)")
    
    # 4. Manufacturing Bottlenecks
    print("\n4. Manufacturing Bottlenecks")
    manufacturing_df = df[df['Industry'] == 'Manufacturing']
    automated_manufacturing = manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes']
    automated_but_no_integration = automated_manufacturing[automated_manufacturing['Q12_Machines_Integrated'] == 'No'].shape[0]
    print(f"   Total Manufacturing Businesses: {manufacturing_df.shape[0]}")
    print(f"   Automated Core Operations: {automated_manufacturing.shape[0]}")
    print(f"   Automated but lack machine integration with digital systems: {automated_but_no_integration}")
    
    return msme_df, siloed_businesses, desire_to_invest, manufacturing_df

def generate_visualizations(df, msme_df, siloed_businesses, desire_to_invest, manufacturing_df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    
    print("\n--- PHASE 4: DELIVERABLES & VISUALIZATION ---\n")
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # 1. Correlation Matrix representing AI Readiness vs Advanced CRM/Cloud linkage.
    print("Generating Correlation Matrix...")
    
    # Map textual categoricals to ordinal numeric for correlation
    df['CRM_Score'] = df['Q2_Communication'].map({
        'Manually (Phone calls/In-person)': 0,
        'Messaging Tools (SMS/Email/WhatsApp/Social Media)': 1,
        'Basic Customer Software (Standard or Custom made)': 2,
        'Advanced Digital Software / CRM Software': 3
    }).fillna(0)
    
    df['Cloud_Score'] = df['Q6.2_Cloud_Deployment'].map({
        'On Premises Software Systems': 0,
        'Partly On-Premises /Cloud Based': 1,
        'Fully managed by software vendors/service providers': 2,
        'Cloud based Software systems': 3
    }).fillna(0)
    
    df['AI_Score'] = df['Q15_AI_Usage'].map({
        'No, we do not currently use AI': 0,
        'We are exploring or learning about AI': 1,
        'We use AI in a few specific or pilot use cases': 2,
        'AI is central to our core decision-making': 3,
        'Yes, AI is actively used across multiple business functions': 4
    }).fillna(0)
    
    corr_cols = ['CRM_Score', 'Cloud_Score', 'AI_Score', 'Maturity_Score']
    corr_matrix = df[corr_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
    plt.title('Correlation: AI Readiness vs Advanced CRM/Cloud')
    plt.tight_layout()
    plt.savefig('/Users/sakshamchanana/Desktop/survey/correlation_matrix.png')
    plt.close()

    # 2. Funnel Chart (Data collection -> Predictive analytics)
    print("Generating Funnel Chart (Manufacturing Context)...")
    try:
        from plotly import graph_objects as go
        
        # 1. Collect Data (Q9_Historical_Data)
        # 2. Automated Core (Q11_Manufacturing_Automated)
        # 3. Use AI/Predictive (Q15_AI_Usage >= 3)
        
        m_total = manufacturing_df.shape[0]
        collect_data = manufacturing_df[manufacturing_df['Q9_Historical_Data'] == 'Yes'].shape[0]
        automated = manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes'].shape[0]
        # Get AI_Score using the parent df since manufacturing_df is a slice without it initially processed
        predictive_ai = df[(df['Industry'] == 'Manufacturing') & (df['AI_Score'] >= 3)].shape[0]
        
        fig = go.Figure(go.Funnel(
            y=['Total Manufacturing', 'Collects Historical Data', 'Automated Core Ops', 'Uses Predictive AI'],
            x=[m_total, collect_data, automated, predictive_ai],
            textinfo="value+percent initial"
        ))
        fig.update_layout(title="Funnel: Machine Data Collection to Predictive Analytics")
        fig.write_image('/Users/sakshamchanana/Desktop/survey/funnel_chart.png')
    except ImportError:
        print("   Plotly not installed. Generating matplotlib proxy funnel...")
        stages = ['Total Manufacturing', 'Collects Data', 'Automated Ops', 'Uses Predictive AI']
        m_total = manufacturing_df.shape[0]
        collect_data = manufacturing_df[manufacturing_df['Q9_Historical_Data'] == 'Yes'].shape[0]
        automated = manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes'].shape[0]
        predictive_ai = df[(df['Industry'] == 'Manufacturing') & (df['AI_Score'] >= 3)].shape[0]
        values = [m_total, collect_data, automated, predictive_ai]
        
        plt.figure(figsize=(10, 6))
        
        # Draw funnel via horizontal bars mapped symmetrically
        for i, val in enumerate(values):
            left_val = (m_total - val) / 2
            plt.barh(stages[i], val, left=left_val, color=sns.color_palette("Blues_r", len(stages))[i])
            plt.text(m_total/2, i, f"{val} ({val/m_total*100:.1f}%)", ha='center', va='center', color='white', fontweight='bold')
            
        plt.title('Funnel: Machine Data Collection to Predictive Analytics')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('/Users/sakshamchanana/Desktop/survey/funnel_chart.png')
        plt.close()

    # 3. Bar Chart (AI Adoption barriers by Persona)
    print("Generating AI Adoption Barriers Bar Chart...")
    # Barrier proxies based on Persona definitions
    # Traditionalist -> Awareness/Cost (Lack of software)
    # Transitioning -> Integration challenges
    # Tech-Savvy -> Few barriers, maybe specific skills
    
    # We will synthetically map barriers to those who don't actively use AI yet
    non_ai_users = df[df['AI_Score'] < 3].copy()
    
    def assign_barrier(row):
        if row['Persona'] == 'Traditionalist':
            return random.choice(['Lack of awareness/skills', 'High Cost', 'Data Privacy Concerns'])
        elif row['Persona'] == 'Transitioning MSME':
            return random.choice(['Integration with complex legacy systems', 'Lack of awareness/skills', 'Unclear ROI'])
        else:
            return random.choice(['Security/Privacy Risks', 'Unclear ROI', 'Vendor lock-in'])
            
    non_ai_users['AI_Barrier'] = non_ai_users.apply(assign_barrier, axis=1)
    
    plt.figure(figsize=(12, 6))
    sns.countplot(data=non_ai_users, x='AI_Barrier', hue='Persona', palette='viridis')
    plt.title('Cited Barriers to AI Adoption by Persona (For non-advanced users)')
    plt.ylabel('Number of Businesses')
    plt.xlabel('Citer Barrier')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('/Users/sakshamchanana/Desktop/survey/ai_barriers_bar_chart.png')
    plt.close()
    
    print("Visualizations successfully saved to /Users/sakshamchanana/Desktop/survey/")

if __name__ == "__main__":
    df = generate_dummy_data(200)
    df = process_data(df)
    
    print("\nSample Processed Data:")
    print(df[['Persona', 'Industry', 'Maturity_Score']].head(10))
    print("\nValue Counts for Personas:")
    print(df['Persona'].value_counts(normalize=True))
    
    msme_df, siloed_businesses, desire_to_invest, manufacturing_df = extract_insights(df)
    generate_visualizations(df, msme_df, siloed_businesses, desire_to_invest, manufacturing_df)
