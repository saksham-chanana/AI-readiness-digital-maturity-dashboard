# Mid-Term Evaluation Presentation Script
**Project: Digital Maturity & AI Readiness Assessment Pipeline**

---

### Slide 1: Title Slide
**Slide Content:** Project Title, Your Name, Date
**Script:**
> "Good morning/afternoon. Today I will be presenting my mid-term progress on the 'Digital Maturity & AI Readiness Assessment Pipeline'. This project is designed to solve a critical enterprise problem: how do organizations accurately quantify their current digital infrastructure to determine if they are actually ready to adopt AI?"

---

### Slide 2: Problem Statement & Objectives
**Slide Content:** 
- The "AI Hype" vs Reality
- Lack of standardized measurement
- Goal: Build an automated, data-driven assessment pipeline
**Script:**
> "The core problem this project addresses is the gap between the desire to invest in AI and the reality of a company's data infrastructure. Many companies want AI but suffer from data silos or lack basic cloud integration. 
> 
> My objective was to build an end-to-end Python pipeline that takes raw survey data about a company's operations, runs it through a weighted scoring engine, and outputs clear, actionable visualizations regarding their 'Digital Maturity' and 'AI Readiness'."

---

### Slide 3: System Architecture (The 3 Phases)
**Slide Content:** Diagram or steps (Generation -> Processing -> Visualization)
**Script:**
> "From a technical architecture standpoint, the pipeline is divided into three distinct modules:
> 1. **Data Generation/Ingestion (`generator.py`)**: For testing, I built a synthetic data generator that creates realistic survey responses based on 3 distinct business personas (Traditionalist, Transitioning, Tech-Savvy). We recently scaled this to handle 100,000 records to test performance.
> 2. **The Processing Engine (`processor.py`)**: This is the core logic. It uses Pandas to ingest the raw CSV, applies a custom weighted algorithm evaluating Cloud Deployment, System Integration, Data Quality, and Security, and assigns a normalized maturity score from 0 to 100.
> 3. **The Analytics & UI (`app.py` & `analytics.py`)**: Finally, the processed data is fed into a Streamlit web application. We use Plotly and Seaborn to extract dynamic insights—like identifying data silos or plotting the manufacturing automation funnel."

---

### Slide 4: The Scoring Algorithm (Deep Dive)
**Slide Content:** Code snippet of `calculate_maturity` or scoring weight breakdown.
**Script:**
> "I want to briefly highlight the `calculate_maturity` algorithm. It’s not just a simple average. It uses a weighted scoring mechanism out of 30 base points.
> 
> For example, having a 'Fully Integrated' system is weighted heavily (4 points), as is 'Advanced Data Security' (3 points). However, merely 'exploring AI' only nets 1 point compared to 'Active AI usage across functions' which grants 6 points. This ensures the final normalized score accurately reflects true operational readiness rather than just 'intent' to use AI."

---

### Slide 5: Key Technical Insights Extracted
**Slide Content:** Screenshots of the Dashboard (Correlation Matrix, Silo Effect pie chart, AI Gap bar chart)
**Script:**
> "The pipeline successfully extracts several critical insights automatically. 
> *   **The Silo Effect Constraint**: The logic identifies businesses using digital tools but lacking integration, calculating exactly what percentage suffer from inconsistent data as a result.
> *   **The AI Reality Gap**: By cross-referencing 'Desire to Invest' against 'Actual Advanced Usage', the tool quantifies the exact gap in readiness.
> *   **Performance**: As of this mid-term evaluation, the Pandas-based engine successfully processes and visualizes datasets of up to 100,000 records efficiently."

---

### Slide 6: Next Steps / Future Scope
**Slide Content:**
- UI File Upload Integration
- Live Database Connection
- Advanced Predictive Modeling
**Script:**
> "Looking ahead to the final evaluation, my next technical steps involve evolving this from a static pipeline into a dynamic application. 
> 
> I plan to implement a UI file-upload feature in the Streamlit dashboard so users can drag-and-drop their actual enterprise survey data and have it processed on the fly. I also intend to refine the scoring weights and potentially integrate a live database connection rather than relying solely on CSV files."

---
---

## Expected Evaluator FAQs & Answers

**Q1: Why did you use synthetic data instead of real enterprise data for this mid-term?**
> **Answer:** "Acquiring 100,000 real, complete enterprise survey responses regarding internal IT infrastructure involves significant data privacy hurdles. By building a persona-based data generator (`generator.py`), I was able to test the robustness, edge cases, and performance of the Pandas processing engine at scale, ensuring it works perfectly before ingesting sensitive client data."

**Q2: How did you determine the exact weights for the scoring algorithm in `processor.py`?**
> **Answer:** "The weights were designed based on standard industry digital transformation frameworks. Foundational elements that block AI—like lack of system integration or poor data security—are weighted heavily because AI models require clean, accessible data. Intent or basic exploration is scored lower to separate true maturity from 'AI hype'."

**Q3: Why did you choose Streamlit for the frontend instead of a traditional framework like React or Angular?**
> **Answer:** "Given the core of the project is a Python data pipeline relying heavily on Pandas and Plotly, Streamlit allowed for the fastest, most cohesive integration. It allows the frontend to directly execute the Python processing functions (`extract_insights`) on the fly without needing to build and maintain a separate REST API backend."

**Q4: How does the system handle missing or poorly formatted data in the CSV?**
> **Answer:** "Currently, the `calculate_maturity` function uses Python's `.get()` method heavily on the DataFrame rows to safely handle missing keys, defaulting to empty strings rather than throwing `KeyErrors`. If an expected answer isn't recognized, it defaults to scoring 0 for that metric, ensuring the pipeline continues running smoothly."

**Q5: You mentioned the dataset size is 100,000 records. Did you run into any performance bottlenecks?**
> **Answer:** "Initially, caching the 70MB processed CSV file in Streamlit caused some reloading issues. I removed the `@st.cache_data` decorator during testing to ensure fresh data loads. While Pandas handles 100,000 rows in memory very quickly, if we scale to millions of rows in the future, transitioning the backend to a SQL database or using Dask would be required."

**Q6: What is the time complexity of your data processing engine?**
> **Answer:** "The processing engine iterates over each row using pandas `iterrows()` temporarily, which is `O(N)` where N is the number of rows. While this is sufficient for 100,000 records taking only a few seconds, vectorizing the `calculate_maturity` function using numpy `where` clauses or pandas `apply` with optimized cython extensions could drastically reduce processing time for larger datasets."

**Q7: How did you ensure the synthetic data behaves like real-world data and not just random noise?**
> **Answer:** "I implemented a persona-based generation strategy. Instead of purely random sampling, I defined distinct personas ('Traditionalist', 'Transitioning MSME', 'Tech-Savvy'). The logic conditionally forces certain answers based on the persona. For example, a 'Traditionalist' has a 0% chance of using 'Cloud-based Advanced CRM', but a high chance of manual tracking. This ensures realistic correlations naturally form in the dataset."

**Q8: If a company wanted to add a completely new section to the survey tomorrow, how hard is that to integrate into the pipeline?**
> **Answer:** "The pipeline is fairly modular. The survey fields are just columns in the pandas DataFrame. You would need to add the new field to the CSV ingestion script, and if it factors into the overall maturity score, update the `calculate_maturity` algorithm to assign a weight to those specific new string values. The visualization layer would automatically adapt if designed generically."

**Q9: Why are you using Plotly Express instead of Matplotlib or Seaborn in Streamlit?**
> **Answer:** "I used Plotly Express because it retains interactivity when embedded in Streamlit. Users can hover over the funnel charts or correlation matrices to see exact tooltips, zoom in on specific data points, and download the charts natively as PNGs. Matplotlib and Seaborn generate static images, which defeats the purpose of an interactive web dashboard."

**Q10: Can this pipeline be deployed to the cloud? What would that architecture look like?**
> **Answer:** "Yes, Streamlit apps are easily containerized with Docker. A standard cloud deployment would involve a Docker container hosted on AWS Fargate or Google Cloud Run. The CSV data ingestion would be swapped out to hit a managed database like Amazon RDS (PostgreSQL), and the processing engine could be triggered upon a database insert via an event-driven architecture."

**Q11: How do you handle potential memory leaks when Streamlit re-runs the script on every user interaction?**
> **Answer:** "Streamlit executes top-down on every state change. To prevent memory leaks or repetitive heavy computation, I initially leveraged the `@st.cache_data` decorator which serializes the loaded DataFrame in RAM. For development testing, I disabled it, but for production, proper cache invalidation strategies (hashing the loaded file) are utilized to prevent excessive RAM consumption."

**Q12: Is your code modularized enough that another developer could easily write unit tests for the scoring engine?**
> **Answer:** "Yes, the core scoring logic is decoupled from the Streamlit UI. The `calculate_maturity(row)` function in `src/processor.py` is a pure function that takes a dictionary-like row and returns a float. This makes it trivial to write `pytest` unit cases passing in mock dictionary rows and asserting the calculated score matches expectations."

**Q13: Why generate 100,000 rows? Isn't 5,000 enough for statistical significance?**
> **Answer:** "Statistically, yes. Engineering-wise, no. Generating a 70MB file with 100,000 records was a stress test for the deployment environment. I needed to verify that the Streamlit app wouldn't crash holding the DataFrame in memory, that Plotly could render complex visualizations (like box plots) without lagging the browser, and verify the GitHub large file constraints."

**Q14: Where does the 'Silo Effect' metric come from technically?**
> **Answer:** "Technically, it is a boolean filtering overlap. I query the DataFrame for businesses where `Q6_Internal_Operations` equals 'Digitally', and `Q6.3_Integration` equals 'Not integrated' or 'Partially integrated'. Then, I subquery that subset for `Q10_Data_Consistency` equals 'No'. This intersection gives us the exact count of businesses harmed by unintegrated software."

**Q15: What libraries are absolutely essential for this application, and how are you managing them?**
> **Answer:** "The core dependencies are `pandas` for processing, `streamlit` for the UI, and `plotly` for rendering charts. I am managing these in an isolated Python virtual environment via `venv` and tracking exact versions in a `requirements.txt` file to ensure the application builds predictably across different operating systems."

**Q16: Did you encounter any issues pushing the 100,000 records CSV file to GitHub?**
> **Answer:** "Yes, the 100,000 record files are around 70MB each. While this is under GitHub's hard limit of 100MB, it triggers a 'Large files detected' warning because it exceeds the recommended 50MB. In a true production environment, large datasets should not be checked into Git. Instead, they should be stored in an AWS S3 bucket or similar blob storage, utilizing Git LFS (Large File Storage) only if absolutely necessary."

**Q17: How would you secure the Streamlit URL if this was deployed internally for executives?**
> **Answer:** "Currently it runs locally. If deployed, open-source Streamlit doesn't have built-in authentication. I would need to deploy the container behind a reverse proxy like Nginx configured with OAuth2, or use a managed service like AWS Cognito, to ensure only authorized corporate accounts can view the strategic insights."

**Q18: If you swap the CSV for a SQL database, how would `app.py` change?**
> **Answer:** "I would replace the `pd.read_csv()` calls with SQLAlchemy or a native connector like `psycopg2`. Let the SQL engine handle the heavy filtering (e.g., `SELECT * WHERE Persona = 'X'`) rather than hauling the entire un-filtered table into Pandas memory and applying masks. This pushes the computation down to the database tier."

**Q19: What is the most fragile part of your current pipeline?**
> **Answer:** "The data ingestion schema is currently brittle. If the upstream survey tool (like Google Forms or Typeform) changes the exact text of a column header (e.g., changing 'Q1_Customer_Discovery' to 'Q1_Discovery'), the Pandas logic will immediately throw a `KeyError`. Implementing a robust schema validation step using a library like `Pydantic` or `Great Expectations` before processing would mitigate this."

**Q20: Can you explain the difference between the 'Maturity Score' and the 'Maturity Category'?**
> **Answer:** "The 'Maturity Score' is the raw continuous variable (a float from 0.0 to 100.0) generated by the algorithm. The 'Maturity Category' applies a set of thresholds (e.g., `<34`, `<67`, `>=67`) to that score to convert it into a categorical string ('Digital Laggard', 'Digital Adopter', 'Digital Leader'). The continuous score is used for correlation mapping, while the categorical string is used for high-level dashboard metrics and grouping."
