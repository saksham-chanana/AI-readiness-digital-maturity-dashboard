# Synopsis: Digital Maturity & AI Readiness Assessment Tool

## 1. Introduction
In today’s rapidly evolving technological landscape, adopting Artificial Intelligence (AI) and digital tools is no longer optional for long-term business survival. However, many organizations struggle to accurately measure their current digital maturity and assess their readiness to adopt advanced AI technologies effectively. The **Digital Maturity & AI Readiness Assessment Tool** addresses this challenge by providing an end-to-end data pipeline, analytics engine, and interactive dashboard designed to evaluate an organization's digital capabilities. By analyzing key domains such as customer discovery, internal operations, data consistency, and current AI utilization, the project surfaces actionable insights to guide enterprise transformation strategies.

## 2. Motivation
The primary motivation behind this project is to eliminate the guesswork involved in digital transformation. Organizations often lack structured data regarding their current capabilities, leading to "blind spots" in departmental needs and bottlenecks. For example, a business might desire to invest in predictive AI but lack the necessary foundational data infrastructure (like advanced CRM or Cloud integration) or suffer from siloed systems that produce inconsistent data. This project aims to convert abstract concepts—like "digital maturity" and "AI readiness"—into measurable, trackable, and highly visual metrics.

## 3. Project Objectives
- **Data Generation & Simulation:** To construct a robust synthetic data generator that simulates realistic enterprise survey responses across various business personas (e.g., Traditionalist, Transitioning MSME, Tech-Savvy Digital Native).
- **Automated Processing & Scoring:** To develop an intelligent backend processing engine capable of calculating modular maturity and AI readiness scores based on complex logic.
- **Insight Extraction:** To automatically identify critical business narratives, such as the impact of siloed software tools, AI adoption barriers, and industry-specific capability funnels (e.g., manufacturing).
- **Interactive Visualization:** To build a real-time web dashboard that serves as an executive control center for exploring key performance indicators (KPIs).
- **Automated Reporting:** To bridge the gap between technical data and leadership by generating automated, polished executive summary presentations.

## 4. Methodology / Planning of Work
The project architecture is built around three primary python-driven phases:

1. **The Data Engine (`generate_and_process.py`):**  
   - Generates 200 synthetic survey responses spanning 18 major questions regarding business operations.
   - Cleans and processes raw data, translating categorical answers into quantifiable numerical scores (`Maturity_Score`, `CRM_Score`, `Cloud_Score`, `AI_Score`).
   - Extracts four distinct business insights using Pandas capabilities and outputs pre-rendered analytical charts (`png` format) using `seaborn` and `plotly`.

2. **The Executive Control Center (`app.py`):**  
   - Implements a web application using **Streamlit**.
   - Integrates the processed CSV data to provide executive KPIs at a glance.
   - Features dynamic and interactive charts, including a Persona Demographics pie chart, an AI Readiness correlation matrix, and an AI Adoption Barriers bar chart, along with a filterable raw data viewer.

3. **The Executive Reporting Module (`generate_presentation.py`):**  
   - Utilizes `python-pptx` to programmatically assemble a PowerPoint slide deck (`AI_Readiness_Executive_Summary.pptx`).
   - Pre-populates the presentation with the project's challenge, solution, capabilities, and business impact based on the defined analytical structure.

## 5. Verification and Validation
- **Logic Validation:** Ensuring the scoring engine accurately weights dependencies. For instance, an organization cannot achieve a high AI Readiness score if they lack fundamental historical data collection or cloud deployment.
- **Data Integrity:** Verification that the generated synthetic dataset holds logical consistency across inter-dependent questions (e.g., Manufacturing businesses showing automation metrics).
- **Visual Validation:** Manually checking the Streamlit dashboard (`app.py`) to ensure all data inputs render accurately without errors and that filtering functionalities (by Persona and Industry) successfully update corresponding dataframes in real-time.
- **Output Inspection:** Validating that the presentation module successfully compiles a `.pptx` file with the correct formatting, text hierarchy, and executive content.

## 6. HW/SW Requirements
### Hardware Requirements
- **CPU:** Standard modern processor (Intel Core i3/Ryzen 3 equivalent or higher)
- **RAM:** Minimum 4GB RAM (8GB recommended for smoother dashboard performance)
- **Storage:** ~100MB of free disk space for scripts, generated datasets, and images.

### Software Requirements
- **Operating System:** macOS (developed on), Windows, or Linux.
- **Runtime Environment:** Python 3.8 or higher.
- **Primary Dependencies:**
  - `pandas` (Data processing and analytics)
  - `numpy` (Numerical operations)
  - `streamlit` (Web dashboard framework)
  - `plotly` (Interactive visualizations)
  - `matplotlib` & `seaborn` (Static chart generation)
  - `python-pptx` (Presentation generation)

## 7. Bibliography
- Scikit-learn Developers. (n.d.). _Pandas Documentation_. Retrieved from [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- Streamlit Inc. (n.d.). _Streamlit Documentation_. Retrieved from [https://docs.streamlit.io/](https://docs.streamlit.io/)
- Plotly Technologies Inc. (n.d.). _Plotly Python Open Source Graphing Library_. Retrieved from [https://plotly.com/python/](https://plotly.com/python/)
- Waskom, M. (n.d.). _Seaborn: statistical data visualization_. Retrieved from [https://seaborn.pydata.org/](https://seaborn.pydata.org/)
- Canny, S. (n.d.). _python-pptx Documentation_. Retrieved from [https://python-pptx.readthedocs.io/](https://python-pptx.readthedocs.io/)
