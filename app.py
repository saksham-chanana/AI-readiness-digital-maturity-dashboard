import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import io
from src.analytics import extract_insights
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
    st.markdown("Fill out the form below to instantly generate a personalized digital maturity scorecard for your organization.")
    
    with st.form("assessment_form"):
        st.subheader("1. Core Operations & Cloud")
        q6 = st.radio("How are your internal operations managed?", 
                      ["Manually", "Digitally (using Software/Tools)"])
        q6_2 = st.selectbox("How is your software deployed?", 
                            ["N/A", "On Premises Software Systems", "Partly On-Premises /Cloud Based", "Cloud based Software systems", "Fully managed by software vendors/service providers"])
        q6_3 = st.selectbox("Are your systems integrated?", 
                            ["Not integrated", "Partially integrated", "Fully integrated"])
                            
        st.subheader("2. Data Management & Security")
        q7 = st.selectbox("How do you manage documents?", 
                          ["Physical files", "Digital files on local devices", "Cloud Storage", "Document management system (DMS)"])
        q10 = st.radio("Is your data consistent across all departments?", ["Yes", "No"])
        q13 = st.selectbox("How do you ensure data quality?",
                           ["No defined process for data accuracy", "Basic checks done manually", "Regular reviews or validations", "Automated checks", "Data quality is continuously monitored"])
        q14 = st.selectbox("What is your data security posture?",
                           ["Minimal / ad-hoc", "Basic security measures in place", "Defined security policies and controls", "Advanced security with regular assessments"])
                           
        st.subheader("3. AI & Advanced Analytics")
        q9 = st.radio("Do you collect structured historical data?", ["Yes", "No"])
        q15 = st.selectbox("What is your current AI adoption level?",
                           ["No, we do not currently use AI", "We are exploring or learning about AI", "We use AI in a few specific or pilot use cases", "AI is central to our core decision-making", "Yes, AI is actively used across multiple business functions"])
        q18 = st.radio("Are you planning to invest in AI in the next 12 months?", ["Yes", "Maybe", "No"])
        
        submitted = st.form_submit_button("Generate Scorecard")
        
    if submitted:
        # Build the mock row dictionary
        form_data = {
            "Q6_Internal_Operations": q6,
            "Q6.2_Cloud_Deployment": q6_2,
            "Q6.3_Integration": q6_3,
            "Q7_Document_Management": q7,
            "Q10_Data_Consistency": q10,
            "Q13_Data_Quality": q13,
            "Q14_Data_Security": q14,
            "Q9_Historical_Data": q9,
            "Q15_AI_Usage": q15,
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
    st.title("📊 Enterprise Analytics Dashboard")
    st.markdown("Macro-level insights across businesses. Upload your own dataset or explore the demo.")
    
    # File Uploader Section
    st.sidebar.subheader("Data Source")
    uploaded_file = st.sidebar.file_uploader("Upload Raw Survey Data (.csv)", type=["csv"])
    
    # Load Data Logic
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            st.sidebar.success("File uploaded successfully! Processing real-time...")
            # Process the raw uploaded data using the engine
            df = process_data(raw_df)
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
    
    # Export Button Logic
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="📥 Download Processed Dataset",
        data=csv_buffer.getvalue(),
        file_name="processed_dataset.csv",
        mime="text/csv",
    )

    # Sidebar Filters
    st.sidebar.header("Data Filters")
    selected_industry = st.sidebar.multiselect("Select Industry", options=df['Industry'].unique(), default=df['Industry'].unique())
    selected_persona = st.sidebar.multiselect("Select Persona", options=df['Persona'].unique(), default=df['Persona'].unique())
    
    filtered_df = df[(df['Industry'].isin(selected_industry)) & (df['Persona'].isin(selected_persona))]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        st.stop()
    
    # Extract dynamic insights
    try:
        insights_tuple = extract_insights(filtered_df)
        insights = insights_tuple[0]
    except Exception as e:
        st.error(f"Error extracting insights, check data format: {e}")
        st.stop()
        
    # --- Top Level Metrics ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Total Businesses</h3><p class="big-font">{filtered_df.shape[0]}</p></div>', unsafe_allow_html=True)
    with col2:
        avg_score = filtered_df['Maturity_Score'].mean()
        st.markdown(f'<div class="metric-card"><h3>Avg Maturity</h3><p class="big-font">{avg_score:.1f}/100</p></div>', unsafe_allow_html=True)
    with col3:
        leaders = filtered_df[filtered_df['Maturity_Category'] == 'Digital Leader'].shape[0]
        st.markdown(f'<div class="metric-card"><h3>Digital Leaders</h3><p class="big-font">{leaders}</p></div>', unsafe_allow_html=True)
    with col4:
        laggards = filtered_df[filtered_df['Maturity_Category'] == 'Digital Laggard'].shape[0]
        st.markdown(f'<div class="metric-card"><h3>Digital Laggards</h3><p class="big-font">{laggards}</p></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # --- Main Dashboard Content ---
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("1. AI Readiness vs Reality Gap")
        st.write("Businesses that want to invest in AI vs those actively using advanced functions.")
        
        fig_ai = px.bar(
            x=["Want to Invest", "Advanced Usage", "The 'Gap'"],
            y=[insights['ai_gap']['desire_to_invest'], insights['ai_gap']['actual_advanced_use'], insights['ai_gap']['gap']],
            labels={'x': "Category", 'y': "Number of Businesses"},
            color=["Want to Invest", "Advanced Usage", "The 'Gap'"],
            color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c']
        )
        st.plotly_chart(fig_ai, use_container_width=True)
    
    with col_right:
        st.subheader("2. Silo Effect: Impact on Data Quality")
        st.write("Businesses using digital tools without proper integration suffer from inconsistent data.")
        
        fig_silo = px.pie(
            values=[insights['silo_effect']['inconsistent_data'], insights['silo_effect']['siloed_businesses'] - insights['silo_effect']['inconsistent_data']],
            names=['Inconsistent Data', 'Consistent Data'],
            title="Data Quality among Siloed Businesses",
            color_discrete_sequence=['#e74c3c', '#95a5a6']
        )
        st.plotly_chart(fig_silo, use_container_width=True)
    
    st.divider()
    
    col_bottom1, col_bottom2 = st.columns([1, 1])
    
    with col_bottom1:
        st.subheader("3. Maturity Distribution by Persona")
        fig_box = px.box(filtered_df, x="Persona", y="Maturity_Score", color="Persona", title="Spread of Digital Maturity (0-100)")
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_bottom2:
        st.subheader("4. Maturity Categories Breakdown")
        category_counts = filtered_df['Maturity_Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        fig_cat = px.bar(category_counts, x='Count', y='Category', orientation='h', color='Category', title="Count of Businesses by Maturity Segment")
        st.plotly_chart(fig_cat, use_container_width=True)
