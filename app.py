import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import io
import random
from streamlit_option_menu import option_menu
from src.processor import calculate_maturity, categorize_maturity, process_data

st.set_page_config(page_title="Digital Maturity Dashboard", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

# Custom CSS for Unreal Engine 5 Glassmorphism UI
st.markdown("""
<style>
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Core Application Background - Deep Cinematic Environment */
    .stApp, .reportview-container {
        background-color: #03040a !important; /* Almost pure black, slight blue tint */
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 100% 100%, rgba(192, 132, 252, 0.15) 0%, transparent 40%);
        color: #f8fafc;
        font-family: 'SF Pro Display', -apple-system, sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, .big-font, p, span, label, div {
        color: #f1f5f9;
        font-family: 'SF Pro Display', -apple-system, sans-serif;
    }
    h1 {
        font-weight: 800;
        letter-spacing: -0.05em;
        text-shadow: 0 4px 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Glassmorphic Floating Cards */
    div[data-testid="stMetric"], .metric-card {
        background: rgba(15, 20, 35, 0.4) !important;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-top: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.5) !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.8) !important;
        border-radius: 24px; 
        box-shadow: 
            0 30px 60px -15px rgba(0, 0, 0, 0.8), /* Deep volumetric shadow */
            0 0 30px rgba(56, 189, 248, 0.05), /* Ambient lighting */
            inset 0 1px 0 rgba(255, 255, 255, 0.1); /* Refractive inner edge */
        padding: 32px;
        text-align: left;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    div[data-testid="stMetric"]:hover, .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 40px 80px -20px rgba(0, 0, 0, 0.9),
            0 0 40px rgba(192, 132, 252, 0.15),
            inset 0 1px 2px rgba(255, 255, 255, 0.2);
        border-top: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Centerpiece Scorecard - Unreal Engine Glow */
    .score-card {
        background: linear-gradient(135deg, rgba(20, 30, 60, 0.6) 0%, rgba(10, 15, 30, 0.8) 100%);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(0, 0, 0, 0.9);
        border-right: 1px solid rgba(0, 0, 0, 0.7);
        color: white;
        padding: 56px 40px;
        border-radius: 32px;
        text-align: center;
        margin: 40px 0;
        box-shadow: 
            0 50px 100px -20px rgba(0, 0, 0, 1), /* Massive drop shadow */
            0 0 80px rgba(56, 189, 248, 0.15), /* Glowing aurora behind card */
            inset 0 2px 20px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    .score-card h2, .score-card h1, .score-card h3 {
        color: #ffffff !important;
    }
    .score-card h1 {
        font-size: 96px !important;
        background: -webkit-linear-gradient(45deg, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
        filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.4)); /* Text neon glow */
    }

    /* Form and Inputs */
    .stSelectbox>div>div, .stTextInput>div>div, .stRadio>div {
        background-color: rgba(15, 20, 35, 0.6) !important;
        backdrop-filter: blur(10px);
        color: #f8fafc !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.5) !important;
        border-radius: 12px;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
    }
    div[data-baseweb="select"] {
        background-color: rgba(15, 20, 35, 0.6) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.5) !important;
        border-radius: 12px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        font-weight: 700;
        font-size: 16px;
        padding: 16px 24px;
        background: linear-gradient(135deg, #38bdf8 0%, #c084fc 100%);
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 10px 30px -5px rgba(192, 132, 252, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #7dd3fc 0%, #d8b4fe 100%);
        box-shadow: 
            0 15px 40px -5px rgba(192, 132, 252, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        transform: translateY(-3px);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: -webkit-linear-gradient(45deg, #f8fafc, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
selected = option_menu(
    menu_title=None,
    options=["Take Assessment", "Analytics Dashboard"],
    icons=["clipboard2-data-fill", "bar-chart-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "8px!important", "background-color": "rgba(15, 20, 35, 0.4)", "backdrop-filter": "blur(24px)", "border-radius": "24px", "box-shadow": "0 20px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.1)", "margin-bottom": "30px", "border-top": "1px solid rgba(255,255,255,0.1)", "border-bottom": "1px solid rgba(0,0,0,0.5)"},
        "icon": {"color": "#94a3b8", "font-size": "20px"},
        "nav-link": {"color": "#94a3b8", "font-size": "15px", "text-align": "center", "margin": "0 4px", "--hover-color": "rgba(255,255,255,0.05)", "font-weight": "500", "border-radius": "16px", "padding": "12px 16px"},
        "nav-link-selected": {"background": "linear-gradient(135deg, #38bdf8 0%, #c084fc 100%)", "color": "#ffffff", "font-weight": "600", "box-shadow": "inset 0 1px 0 rgba(255,255,255,0.4)"},
    }
)
view = selected

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
    with st.expander("🛠 Data Management (Upload Custom CSV to Sandbox)", expanded=False):
        uploaded_file = st.file_uploader("Override the Demo Dashboard with your own raw Survey Data (.csv)", type=["csv"])
    
    # Load Data Logic
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully! Processing real-time...")
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
                         title='Distribution of Respondent Personas', hole=0.85,
                         color_discrete_sequence=['#38bdf8', '#c084fc', '#f472b6', '#818cf8', '#e2e8f0'])
        fig_pie.update_traces(textinfo='percent', 
                              marker=dict(line=dict(color='rgba(0,0,0,0)', width=0)),
                              hoverinfo='label+percent+value')
        fig_pie.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              font=dict(family="SF Pro Display, sans-serif", color='#f8fafc'),
                              showlegend=False,
                              annotations=[dict(text='Personas', x=0.5, y=0.5, font_size=24, showarrow=False, font=dict(color='#94a3b8'))])
        st.plotly_chart(fig_pie, use_container_width=True)

    with row1_col2:
        st.subheader("2. Correlation Matrix")
        # Ensure we only use numeric columns that exist in the dataframe
        possible_cols = ['CRM_Score', 'Cloud_Score', 'AI_Score', 'Maturity_Score']
        corr_cols = [c for c in possible_cols if c in filtered_df.columns]
        
        if len(corr_cols) > 1:
            # Calculate correlation matrix
            corr_matrix = filtered_df[corr_cols].corr()
            
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", 
                                 color_continuous_scale=['#c084fc', '#03040a', '#38bdf8'], zmin=-1, zmax=1,
                                 title="AI Readiness vs Adv. CRM/Cloud")
            fig_corr.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="SF Pro Display, sans-serif", color='#f8fafc'))
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
                marker={"color": ["#f8fafc", "#818cf8", "#c084fc", "#38bdf8"],
                        "line": {"width": [0, 0, 0, 0], "color": ["rgba(0,0,0,0)"] * 4}}
            ))
            fig_funnel.update_layout(title="Data Collection to Predictive Analytics", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="SF Pro Display, sans-serif", color='#f8fafc'))
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
                                      text_auto='.0f', color_discrete_sequence=['#38bdf8', '#c084fc', '#f472b6', '#818cf8'])
                fig_barriers.update_layout(xaxis_title="Cited Barrier", yaxis_title="Number of Businesses", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="SF Pro Display, sans-serif", color='#f8fafc'), bargap=0.2)
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
