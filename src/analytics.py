import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os

def extract_insights(df):
    """
    Extracts key business narratives from the processed data.
    """
    insights = {}
    
    # 1. Tool Adoption & Market Penetration
    msme_df = df[df['Persona'] == 'Transitioning MSME']
    traditional_accounting = msme_df[msme_df['Q6.1.8_Accounting_Tools'] == 'Tally Prime'].shape[0]
    cloud_accounting = msme_df[msme_df['Q6.1.8_Accounting_Tools'].isin(['Zoho Books', 'Vyapar'])].shape[0]
    total_msme = msme_df.shape[0]
    
    insights['tool_adoption'] = {
        'total_msme': total_msme,
        'traditional': traditional_accounting,
        'cloud': cloud_accounting
    }
    
    # 2. The "Silo" Effect
    multiple_tools = df[df['Q6_Internal_Operations'] == 'Digitally (using Software/Tools)']
    siloed_businesses = multiple_tools[(multiple_tools['Q6.3_Integration'] == 'Not integrated') | (multiple_tools['Q6.3_Integration'] == 'Partially integrated')]
    inconsistent_data_in_silos = siloed_businesses[siloed_businesses['Q10_Data_Consistency'] == 'No'].shape[0]
    
    insights['silo_effect'] = {
        'siloed_businesses': siloed_businesses.shape[0],
        'inconsistent_data': inconsistent_data_in_silos
    }

    # 3. AI Readiness vs Reality
    desire_to_invest = df[df['Q18_AI_Investment'] == 'Yes']
    actual_ai_usage = df[df['Q15_AI_Usage'].isin(['Yes, AI is actively used across multiple business functions', 'AI is central to our core decision-making'])]
    gap = desire_to_invest[~desire_to_invest['Q15_AI_Usage'].isin(['Yes, AI is actively used across multiple business functions', 'AI is central to our core decision-making'])]
    
    insights['ai_gap'] = {
        'desire_to_invest': desire_to_invest.shape[0],
        'actual_advanced_use': actual_ai_usage.shape[0],
        'gap': gap.shape[0],
        'total': df.shape[0]
    }
    
    # 4. Manufacturing Bottlenecks
    manufacturing_df = df[df['Industry'] == 'Manufacturing']
    automated_manufacturing = manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes']
    automated_but_no_integration = automated_manufacturing[automated_manufacturing['Q12_Machines_Integrated'] == 'No'].shape[0]
    
    insights['manufacturing'] = {
        'total': manufacturing_df.shape[0],
        'automated': automated_manufacturing.shape[0],
        'bottleneck': automated_but_no_integration
    }
    
    return insights, msme_df, siloed_businesses, desire_to_invest, manufacturing_df


def generate_visualizations(df, insights_tuple, output_dir="../output"):
    """
    Generates improved charts and saves them to the output directory.
    """
    insights, msme_df, siloed_businesses, desire_to_invest, manufacturing_df = insights_tuple
    
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    # 1. Maturity Distribution by Persona
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Persona', y='Maturity_Score', palette='Set2')
    plt.title('Distribution of Digital Maturity Scores by Persona')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/maturity_distribution.png')
    plt.close()

    # 2. Funnel Chart (Plotly)
    m_total = insights['manufacturing']['total']
    collect_data = manufacturing_df[manufacturing_df['Q9_Historical_Data'] == 'Yes'].shape[0]
    automated = insights['manufacturing']['automated']
    predictive_ai = df[(df['Industry'] == 'Manufacturing') & (df['Maturity_Score'] >= 80)].shape[0]
    
    fig = go.Figure(go.Funnel(
        y=['Total Manufacturing', 'Collects Historical Data', 'Automated Core Ops', 'Uses Predictive AI (High Maturity)'],
        x=[m_total, collect_data, automated, predictive_ai],
        textinfo="value+percent initial"
    ))
    fig.update_layout(title="Manufacturing Funnel: Data Collection to Predictive Analytics")
    try:
        fig.write_image(f'{output_dir}/manufacturing_funnel.png')
    except Exception as e:
        print("Note: kaleido package is required for rendering plotly logic to png. Assuming it might not be installed.")
        pass

    # 3. AI Usage Categories Bar Chart
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, y='Q15_AI_Usage', hue='Persona', palette='viridis')
    plt.title('AI Usage Levels by Persona')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ai_usage_bar_chart.png')
    plt.close()

    print(f"Visualizations successfully saved to {output_dir}")

if __name__ == "__main__":
    if os.path.exists("../data/processed_responses.csv"):
        df = pd.read_csv("../data/processed_responses.csv")
        ins = extract_insights(df)
        generate_visualizations(df, ins)
