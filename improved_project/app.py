import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from src.analytics import extract_insights

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
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "data/processed_responses.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

df = load_data()

if df is None:
    st.error("Processed data not found! Please run `python main.py` first to generate data.")
    st.stop()

st.title("📊 Digital Maturity & AI Readiness Assessment")
st.markdown("Interactive dashboard exploring Insights from the Survey Data.")

# Sidebar Filters
st.sidebar.header("Filters")
selected_industry = st.sidebar.multiselect("Select Industry", options=df['Industry'].unique(), default=df['Industry'].unique())
selected_persona = st.sidebar.multiselect("Select Persona", options=df['Persona'].unique(), default=df['Persona'].unique())

filtered_df = df[(df['Industry'].isin(selected_industry)) & (df['Persona'].isin(selected_persona))]

# Extract dynamic insights
insights_tuple = extract_insights(filtered_df)
insights = insights_tuple[0]

# --- Top Level Metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><h3>Total Responses</h3><p class="big-font">{filtered_df.shape[0]}</p></div>', unsafe_allow_html=True)
with col2:
    avg_score = filtered_df['Maturity_Score'].mean()
    st.markdown(f'<div class="metric-card"><h3>Avg Maturity Score</h3><p class="big-font">{avg_score:.1f}/100</p></div>', unsafe_allow_html=True)
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
    st.write("Businesses that want to invest in AI vs those actively using it advanced functions.")
    
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
