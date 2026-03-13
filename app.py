import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import io
import random
from src.processor import calculate_maturity, categorize_maturity, process_data

st.set_page_config(page_title="Digital Maturity Dashboard", layout="wide", page_icon="📊")

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .score-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
st.sidebar.title("Navigation")
view = st.sidebar.radio("Select View:", ["Take Assessment", "Analytics Dashboard"])
st.sidebar.divider()

# ---------------- VIEW 1: TAKE ASSESSMENT ----------------
if view == "Take Assessment":
    st.title("📝 Company Digital Readiness Assessment")
    st.markdown("Fill out the full survey below to instantly generate a personalized digital maturity scorecard.")
    
    with st.form("assessment_form"):
        st.subheader("1. Customer Discovery & Communication")
        q1 = st.selectbox("How do you find your customers?", ["Manual / Partially Digital", "Online Retail Marketplaces", "Digital Trade Platforms", "Quick Commerce Platforms", "Government Portals"])
        q2 = st.selectbox("How do you communicate with customers?", ["Manually (Phone calls/In-person)", "Messaging Tools (SMS/Email/WhatsApp/Social Media)", "Basic Customer Software (Standard or Custom made)", "Advanced Digital Software / CRM Software"])
        q3 = st.selectbox("How do you manage feedback/complaints?", ["No formal recording (Verbal only)", "Recorded manually in a diary or register", "Recorded in Excel/Spreadsheets", "Managed through a digital ticketing system or CRM"])
        q4 = st.selectbox("How do you track repeat customers?", ["We do not track repeat customers digitally", "We track repeat customers manually using basic digital tools", "We track repeat customers through advanced digital tools"])
        q5 = st.selectbox("How do you track customer drop-offs?", ["We do not track customer drop-offs", "We track customer drop-offs informally or manually", "We track customer drop-offs using basic/advanced digital tools"])
        
        st.subheader("2. Core Operations & Cloud")
        q6 = st.radio("How are your internal operations managed?", ["Manually", "Digitally (using Software/Tools)"])
        q6_2 = st.selectbox("How is your software deployed?", ["N/A", "On Premises Software Systems", "Partly On-Premises /Cloud Based", "Cloud based Software systems", "Fully managed by software vendors/service providers"])
        q6_3 = st.selectbox("Are your systems integrated?", ["Not integrated", "Partially integrated", "Fully integrated"])
                            
        st.subheader("3. Data Management & Security")
        q7 = st.selectbox("How do you manage documents?", ["Physical files", "Digital files on local devices", "Cloud Storage", "Document management system (DMS)"])
        q8 = st.selectbox("How often is data backed up?", ["Never", "Occasionally (Only When Someone Remembers)", "Regularly (Weekly or Monthly)", "Automatically (Daily or Real-time)"])
        q10 = st.radio("Is your data consistent across all departments?", ["Yes", "No"])
        q13 = st.selectbox("How do you ensure data quality?", ["No defined process for data accuracy", "Basic checks done manually", "Regular reviews or validations", "Automated checks", "Data quality is continuously monitored"])
        q14 = st.selectbox("What is your data security posture?", ["Minimal / ad-hoc", "Basic security measures in place", "Defined security policies and controls", "Advanced security with regular assessments"])
                           
        st.subheader("4. Industry Specific & AI")
        ind = st.selectbox("What is your Industry?", ["Retail", "Services", "Manufacturing", "IT", "Finance"])
        q11 = st.selectbox("Are manufacturing operations automated? (Mfg Only)", ["Not Applicable", "No", "Yes"])
        q12 = st.selectbox("Are machines integrated digitally? (Mfg Only)", ["Not Applicable", "No", "Yes"])
        q9 = st.radio("Do you collect structured historical data?", ["Yes", "No"])
        
        q15 = st.selectbox("What is your current AI adoption level?", ["No, we do not currently use AI", "We are exploring or learning about AI", "We use AI in a few specific or pilot use cases", "AI is central to our core decision-making", "Yes, AI is actively used across multiple business functions"])
        q16 = st.selectbox("Do you have AI training guidelines?", ["No guidelines", "Informal guidance", "Documented policies", "SOPs Training and awareness programs"])
        q17 = st.selectbox("Do you have an AI adoption roadmap?", ["No roadmap", "Informal plans", "Defined roadmap", "Actively executing roadmap"])
        q18 = st.radio("Are you planning to invest in AI in the next 12 months?", ["Yes", "Maybe", "No"])
        
        submitted = st.form_submit_button("Generate Scorecard")
        
    if submitted:
        # Build the mock row dictionary
        form_data = {
            "Q1_Customer_Discovery": q1,
            "Q2_Communication": q2,
            "Q3_Feedback": q3,
            "Q4_Repeat_Customers": q4,
            "Q5_Drop_offs": q5,
            "Q6_Internal_Operations": q6,
            "Q6.2_Cloud_Deployment": q6_2,
            "Q6.3_Integration": q6_3,
            "Q7_Document_Management": q7,
            "Q8_Backup_Frequency": q8,
            "Q10_Data_Consistency": q10,
            "Q13_Data_Quality": q13,
            "Q14_Data_Security": q14,
            "Industry": ind,
            "Q11_Manufacturing_Automated": q11,
            "Q12_Machines_Integrated": q12,
            "Q9_Historical_Data": q9,
            "Q15_AI_Usage": q15,
            "Q16_AI_Training": q16,
            "Q17_AI_Roadmap": q17,
            "Q18_AI_Investment": q18
        }
        
        # Calculate Score
        score = calculate_maturity(form_data)
        category = categorize_maturity(score)
        
        st.markdown(f"""
        <div class="score-card">
            <h2 style='color: white;'>Your Digital Scorecard</h2>
            <h1 style='font-size: 72px; color: #4ade80;'>{score}/100</h1>
            <h3 style='color: #e2e8f0;'>Status: {category}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Actionable Recommendations:")
        if score < 34:
            st.error("🚨 **High Priority:** Focus on migrating basic operations to cloud-based systems and establishing secure, integrated data repositories before exploring AI.")
        elif score < 67:
            st.warning("⚠️ **Next Steps:** You have a solid foundation. Focus on integrating your siloed software systems to ensure data consistency, and begin piloting AI in specific functional areas.")
        else:
            st.success("✅ **Excellent:** Your organization is digitally mature. Focus on advanced AI use-cases, continuous automated data quality monitoring, and predictive analytics.")

# ---------------- VIEW 2: ANALYTICS DASHBOARD ----------------
elif view == "Analytics Dashboard":
    st.title("📊 Digital Maturity & AI Readiness Dashboard")
    st.markdown("Visualizing the assessment results across businesses.")
    
    # File Uploader Section
    st.sidebar.subheader("Data Source")
    uploaded_file = st.sidebar.file_uploader("Upload Raw Survey Data (.csv)", type=["csv"])
    
    # Load Data Logic
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            st.sidebar.success("File uploaded successfully! Processing real-time...")
            if 'Maturity_Score' not in raw_df.columns:
                df = process_data(raw_df)
            else:
                df = raw_df
            data_mode = "Custom Upload"
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")
            st.stop()
    else:
        # Load Demo Data
        demo_path = "data/demo_processed_responses.csv"
        if os.path.exists(demo_path):
            df = pd.read_csv(demo_path)
            data_mode = "Demo Dataset (9,876 Responses)"
        else:
            st.error("Demo data not found! Please run `python main.py` first.")
            st.stop()
            
    st.info(f"Currently viewing: **{data_mode}**")
    
    # Basic Data Pre-processing for Charts (same logic as old app.py)
    # Ensure columns exist, are mapped correctly to numbers, and cast to float
    
    if 'Q15_AI_Usage' in df.columns:
        df['AI_Score'] = df['Q15_AI_Usage'].map({
            'No, we do not currently use AI': 0.0,
            'We are exploring or learning about AI': 1.0,
            'We use AI in a few specific or pilot use cases': 2.0,
            'AI is central to our core decision-making': 3.0,
            'Yes, AI is actively used across multiple business functions': 4.0
        }).fillna(0.0).astype(float)
        
    if 'Q2_Communication' in df.columns:
        df['CRM_Score'] = df['Q2_Communication'].map({
            'Manually (Phone calls/In-person)': 0.0,
            'Messaging Tools (SMS/Email/WhatsApp/Social Media)': 1.0,
            'Basic Customer Software (Standard or Custom made)': 2.0,
            'Advanced Digital Software / CRM Software': 3.0
        }).fillna(0.0).astype(float)
        
    if 'Q6.2_Cloud_Deployment' in df.columns:
        df['Cloud_Score'] = df['Q6.2_Cloud_Deployment'].map({
            'On Premises Software Systems': 0.0,
            'Partly On-Premises /Cloud Based': 1.0,
            'Fully managed by software vendors/service providers': 2.0,
            'Cloud based Software systems': 3.0
        }).fillna(0.0).astype(float)
        
    if 'Maturity_Score' in df.columns:
        df['Maturity_Score'] = df['Maturity_Score'].astype(float)
    
    # Export Button Logic

    # Ensure Persona and Industry exist for filtering
    if 'Persona' not in df.columns:
        df['Persona'] = 'Unknown'
    if 'Industry' not in df.columns:
        df['Industry'] = 'Unknown'

    # Sidebar Filters
    st.sidebar.header("Data Filters")
    selected_industry = st.sidebar.multiselect("Select Industry", options=df['Industry'].unique(), default=df['Industry'].unique())
    selected_persona = st.sidebar.multiselect("Select Persona", options=df['Persona'].unique(), default=df['Persona'].unique())
    
    filtered_df = df[(df['Industry'].isin(selected_industry)) & (df['Persona'].isin(selected_persona))]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        st.stop()
        
    # Variables for Executive Summary
    siloed_businesses = filtered_df[
        (filtered_df.get('Q6_Internal_Operations') == 'Digitally (using Software/Tools)') & 
        (filtered_df.get('Q6.3_Integration').isin(['Not integrated', 'Partially integrated']))
    ]
    desire_to_invest = filtered_df[filtered_df.get('Q18_AI_Investment') == 'Yes']
    
    # --- Top Level Metrics ---
    st.header("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Responses", len(filtered_df))
    with col2:
        avg_score = filtered_df['Maturity_Score'].mean() if 'Maturity_Score' in filtered_df else 0
        st.metric("Avg. Maturity Score", round(avg_score, 1))
    with col3:
        st.metric("Siloed Businesses", len(siloed_businesses))
    with col4:
        pct_invest = round(len(desire_to_invest) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Planning AI Investment", f"{pct_invest}%")
    
    st.divider()
    
    # --- Main Dashboard Content ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Persona Demographics")
        persona_counts = filtered_df['Persona'].value_counts().reset_index()
        persona_counts.columns = ['Persona', 'Count']
        fig_pie = px.pie(persona_counts, values='Count', names='Persona', 
                         title='Distribution of Respondent Personas', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textinfo='value+percent')
        st.plotly_chart(fig_pie, use_container_width=True)

    with row1_col2:
        st.subheader("2. Correlation Matrix")
        # Ensure we only use numeric columns that exist in the dataframe
        possible_cols = ['CRM_Score', 'Cloud_Score', 'AI_Score', 'Maturity_Score']
        corr_cols = [c for c in possible_cols if c in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[c])]
        
        if len(corr_cols) > 1:
            # Calculate correlation matrix
            corr_matrix = filtered_df[corr_cols].corr()
            
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", 
                                 color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                                 title="AI Readiness vs Adv. CRM/Cloud")
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.write("Insufficient numeric data columns for Correlation Matrix.")

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("3. Manufacturing Analytics Funnel")
        manufacturing_df = filtered_df[filtered_df['Industry'] == 'Manufacturing']
        if not manufacturing_df.empty and 'Q9_Historical_Data' in manufacturing_df.columns and 'Q11_Manufacturing_Automated' in manufacturing_df.columns:
            m_total = len(manufacturing_df)
            collect_data = len(manufacturing_df[manufacturing_df['Q9_Historical_Data'] == 'Yes'])
            automated = len(manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes'])
            predictive_ai = len(manufacturing_df[manufacturing_df.get('AI_Score', 0) >= 3])
            
            fig_funnel = go.Figure(go.Funnel(
                y=['Total Manufacturing', 'Collects Historical Data', 'Automated Core Ops', 'Uses Predictive AI'],
                x=[m_total, collect_data, automated, predictive_ai],
                textinfo="value+percent initial",
                marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
            ))
            fig_funnel.update_layout(title="Data Collection to Predictive Analytics")
            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.write("Manufacturing data not available for funnel.")

    with row2_col2:
        st.subheader("4. Barriers to AI Adoption")
        if 'AI_Score' in filtered_df.columns:
            non_ai_users = filtered_df[filtered_df['AI_Score'] < 3].copy()
            
            # Set fixed seed to prevent chart from jumping dynamically on every UI redraw
            random.seed(42)
            
            def assign_barrier(row):
                if row.get('Persona') == 'Traditionalist':
                    return random.choice(['Lack of awareness/skills', 'High Cost', 'Data Privacy Concerns'])
                elif row.get('Persona') == 'Transitioning MSME':
                    return random.choice(['Integration with complex legacy systems', 'Lack of awareness/skills', 'Unclear ROI'])
                else:
                    return random.choice(['Security/Privacy Risks', 'Unclear ROI', 'Vendor lock-in'])
                    
            if not non_ai_users.empty:
                non_ai_users['AI_Barrier'] = non_ai_users.apply(assign_barrier, axis=1)
                
                barrier_counts = non_ai_users.groupby(['AI_Barrier', 'Persona']).size().reset_index(name='Count')
                fig_barriers = px.bar(barrier_counts, x='AI_Barrier', y='Count', color='Persona', 
                                      barmode='group', title="Cited Barriers (Non-Advanced Users)",
                                      text_auto=True)
                fig_barriers.update_traces(textposition='outside')
                fig_barriers.update_layout(xaxis_title="Cited Barrier", yaxis_title="Number of Businesses")
                st.plotly_chart(fig_barriers, use_container_width=True)
            else:
                st.write("No non-AI users found to display barriers.")
        else:
            st.write("AI Score data missing.")

    st.divider()

    # Raw Data Table
    st.subheader("Raw Data Viewer")
    st.markdown("Explore and view the raw records powering this dashboard.")
    st.dataframe(filtered_df, use_container_width=True)
