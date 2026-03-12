import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(page_title="Digital Maturity & AI Readiness Assessment", layout="wide", page_icon="📊")

# Load data function
def load_data():
    try:
        # Assumes data exists in the current working directory
        df = pd.read_csv('processed_responses.csv')
        msme_df = df[df['Persona'] == 'Transitioning MSME']
        siloed_businesses = df[
            (df['Q6_Internal_Operations'] == 'Digitally (using Software/Tools)') & 
            (df['Q6.3_Integration'].isin(['Not integrated', 'Partially integrated']))
        ]
        desire_to_invest = df[df['Q18_AI_Investment'] == 'Yes']
        manufacturing_df = df[df['Industry'] == 'Manufacturing']
        
        # Recalculate AI Score if missing from CSV to ensure plots work
        if 'AI_Score' not in df.columns:
            df['AI_Score'] = df['Q15_AI_Usage'].map({
                'No, we do not currently use AI': 0,
                'We are exploring or learning about AI': 1,
                'We use AI in a few specific or pilot use cases': 2,
                'AI is central to our core decision-making': 3,
                'Yes, AI is actively used across multiple business functions': 4
            }).fillna(0)
            
        if 'CRM_Score' not in df.columns:
            df['CRM_Score'] = df['Q2_Communication'].map({
                'Manually (Phone calls/In-person)': 0,
                'Messaging Tools (SMS/Email/WhatsApp/Social Media)': 1,
                'Basic Customer Software (Standard or Custom made)': 2,
                'Advanced Digital Software / CRM Software': 3
            }).fillna(0)
            
        if 'Cloud_Score' not in df.columns:
            df['Cloud_Score'] = df['Q6.2_Cloud_Deployment'].map({
                'On Premises Software Systems': 0,
                'Partly On-Premises /Cloud Based': 1,
                'Fully managed by software vendors/service providers': 2,
                'Cloud based Software systems': 3
            }).fillna(0)

        manufacturing_df = df[df['Industry'] == 'Manufacturing']
        
        return df, msme_df, siloed_businesses, desire_to_invest, manufacturing_df
    except FileNotFoundError:
        st.error("Processed data file not found. Please run the generation script first.")
        return None, None, None, None, None

df, msme_df, siloed_businesses, desire_to_invest, manufacturing_df = load_data()

if df is not None:
    # Header
    st.title("📊 Digital Maturity & AI Readiness Dashboard")
    st.markdown("Visualizing the synthetic assessment results across MSMEs.")
    
    # KPIs
    st.header("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Responses", len(df))
    with col2:
        st.metric("Avg. Maturity Score", round(df['Maturity_Score'].mean(), 1))
    with col3:
        st.metric("Siloed Businesses", len(siloed_businesses))
    with col4:
        st.metric("Planning AI Investment", f"{round(len(desire_to_invest) / len(df) * 100)}%")

    st.divider()

    # Layout for charts
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Persona Demographics")
        persona_counts = df['Persona'].value_counts().reset_index()
        persona_counts.columns = ['Persona', 'Count']
        fig_pie = px.pie(persona_counts, values='Count', names='Persona', 
                         title='Distribution of Respondent Personas', hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    with row1_col2:
        st.subheader("2. Correlation Matrix")
        corr_cols = ['CRM_Score', 'Cloud_Score', 'AI_Score', 'Maturity_Score']
        corr_matrix = df[corr_cols].corr()
        
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", 
                             color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                             title="AI Readiness vs Adv. CRM/Cloud")
        st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("3. Manufacturing Analytics Funnel")
        m_total = len(manufacturing_df)
        collect_data = len(manufacturing_df[manufacturing_df['Q9_Historical_Data'] == 'Yes'])
        automated = len(manufacturing_df[manufacturing_df['Q11_Manufacturing_Automated'] == 'Yes'])
        predictive_ai = len(manufacturing_df[manufacturing_df['AI_Score'] >= 3])
        
        fig_funnel = go.Figure(go.Funnel(
            y=['Total Manufacturing', 'Collects Historical Data', 'Automated Core Ops', 'Uses Predictive AI'],
            x=[m_total, collect_data, automated, predictive_ai],
            textinfo="value+percent initial",
            marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
        ))
        fig_funnel.update_layout(title="Data Collection to Predictive Analytics")
        st.plotly_chart(fig_funnel, use_container_width=True)

    with row2_col2:
        st.subheader("4. Barriers to AI Adoption")
        import random
        # Generating ad-hoc barriers as in phase 4 of script
        non_ai_users = df[df['AI_Score'] < 3].copy()
        
        def assign_barrier(row):
            if row['Persona'] == 'Traditionalist':
                return random.choice(['Lack of awareness/skills', 'High Cost', 'Data Privacy Concerns'])
            elif row['Persona'] == 'Transitioning MSME':
                return random.choice(['Integration with complex legacy systems', 'Lack of awareness/skills', 'Unclear ROI'])
            else:
                return random.choice(['Security/Privacy Risks', 'Unclear ROI', 'Vendor lock-in'])
                
        non_ai_users['AI_Barrier'] = non_ai_users.apply(assign_barrier, axis=1)
        
        barrier_counts = non_ai_users.groupby(['AI_Barrier', 'Persona']).size().reset_index(name='Count')
        fig_barriers = px.bar(barrier_counts, x='AI_Barrier', y='Count', color='Persona', 
                              barmode='group', title="Cited Barriers (Non-Advanced Users)")
        fig_barriers.update_layout(xaxis_title="Cited Barrier", yaxis_title="Number of Businesses")
        st.plotly_chart(fig_barriers, use_container_width=True)

    st.divider()

    # Raw Data Table
    st.subheader("Raw Data Viewer")
    st.markdown("Filter and explore the generated synthetic responses.")
    
    # Basic filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_persona = st.selectbox("Filter by Persona", ["All"] + list(df['Persona'].unique()))
    with col_f2:
        selected_industry = st.selectbox("Filter by Industry", ["All"] + list(df['Industry'].unique()))

    # Apply filters
    filtered_df = df.copy()
    if selected_persona != "All":
        filtered_df = filtered_df[filtered_df['Persona'] == selected_persona]
    if selected_industry != "All":
        filtered_df = filtered_df[filtered_df['Industry'] == selected_industry]

    st.dataframe(filtered_df, use_container_width=True)
