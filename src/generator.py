import pandas as pd
import numpy as np
import random
from faker import Faker
import os

def generate_dummy_data(num_samples=200, output_path=None):
    np.random.seed(42)
    random.seed(42)
    fake = Faker('en_IN')  # Use Indian localization
    Faker.seed(42)
    
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
            
        row = {
            "Company_Name": fake.company(),
            "City": fake.city(),
            "State": fake.state(),
            "Persona": persona
        }
        
        # Industry specific
        if persona == "Traditionalist":
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing"])
        elif persona == "Transitioning MSME":
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing", "IT"])
        else:
            row["Industry"] = random.choice(["Retail", "Services", "Manufacturing", "IT", "Finance"])

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
        elif persona == "Transitioning MSME":
            row["Q7_Document_Management"] = random.choice(["Digital files on local devices", "Cloud Storage"])
            row["Q8_Backup_Frequency"] = random.choice(["Occasionally (Only When Someone Remembers)", "Regularly (Weekly or Monthly)"])
            row["Q9_Historical_Data"] = random.choice(["Yes", "No"])
            row["Q10_Data_Consistency"] = random.choice(["Yes", "No"])
        else:
            row["Q7_Document_Management"] = random.choice(["Cloud Storage", "Document management system (DMS)"])
            row["Q8_Backup_Frequency"] = random.choice(["Regularly (Weekly or Monthly)", "Automatically (Daily or Real-time)"])
            row["Q9_Historical_Data"] = "Yes"
            row["Q10_Data_Consistency"] = "Yes"

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
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Successfully generated dummy data -> {output_path}")
        
    return df

if __name__ == "__main__":
    generate_dummy_data(output_path="../data/dummy_responses.csv")
