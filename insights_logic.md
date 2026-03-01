# Insights Logic Extraction

This document outlines the logic used in the `generate_and_process.py` script for extracting insights from the survey data. The logic is primarily housed in the `extract_insights(df)` function.

The function takes the processed pandas DataFrame (`df`) containing survey responses and performs filtering, aggregation, and segmentation to extract four key business narratives.

## 1. Tool Adoption & Market Penetration (Traditional vs Cloud for MSMEs)

This insight focuses specifically on how "Transitioning MSMEs" are adopting accounting tools, comparing traditional on-premise software with modern cloud-based solutions.

**Logic:**
1.  **Filter by Persona:** The dataset is filtered to include only rows where the `Persona` is exactly `"Transitioning MSME"`. This creates a subset DataFrame (`msme_df`).
2.  **Count Traditional Adopters:** It counts the number of businesses in this subset that use traditional, on-premise accounting software (specifically where `Q6.1.8_Accounting_Tools` == `"Tally Prime"`).
3.  **Count Cloud Adopters:** It counts the number of businesses using cloud-based alternatives (where `Q6.1.8_Accounting_Tools` is either `"Zoho Books"` or `"Vyapar"`).
4.  **Calculate Percentages:** It calculates the percentage of the total Transitioning MSME market that each of these segments represents relative to the total number of Transitioning MSMEs.

## 2. The "Silo" Effect (System Integration vs Data Consistency)

This insight aims to demonstrate that using digital tools without proper integration leads to data inconsistency, proving the negative impact of disconnected software.

**Logic:**
1.  **Identify Digital Users:** It first filters for businesses that use digital tools for their internal operations (where `Q6_Internal_Operations` == `"Digitally (using Software/Tools)"`).
2.  **Identify Siloed Businesses:** From that group of digital users, it identifies "siloed" businesses. These are defined as businesses whose tools are either `"Not integrated"` or `"Partially integrated"` (based on the `Q6.3_Integration` column).
3.  **Cross-reference with Data Consistency:** It then looks at these siloed businesses and identifies how many suffer from inconsistent data (where `Q10_Data_Consistency` == `"No"`).
4.  **Calculate Metric:** Finally, it calculates the percentage of these siloed businesses that report inconsistent data, highlighting the correlation between poor integration and poor data quality.

## 3. AI Readiness vs Reality (Future Investment vs Current Usage)

This insight calculates the gap between businesses that *express a desire* to invest in AI and those that are *currently* using it in an advanced capacity.

**Logic:**
1.  **Identify Investment Intent:** It isolates businesses that have indicated they plan to invest in AI in the future (where `Q18_AI_Investment` == `"Yes"`).
2.  **Identify Advanced Current Usage:** It isolates businesses that are currently using advanced AI. This is defined by answering either `"Yes, AI is actively used across multiple business functions"` or `"AI is central to our core decision-making"` to the `Q15_AI_Usage` question.
3.  **Calculate the Gap:** It takes the group that *wants* to invest (Step 1) and filters out anyone who is already in the advanced usage group (Step 2). This isolated group represents businesses that have the *intent* to buy AI but aren't heavily using it yet.
4.  **Calculate Percentages:** It reports the percentages of each of these groups relative to the entire dataset to illustrate the 'readiness vs reality' gap.

## 4. Manufacturing Bottlenecks

This insight zooms in on the manufacturing sector to find where automation efforts stall and become bottlenecks.

**Logic:**
1.  **Filter by Industry:** It isolates rows where the `Industry` is `"Manufacturing"`.
2.  **Identify Core Automation:** Within the manufacturing subset, it finds businesses that have automated their core manufacturing operations (where `Q11_Manufacturing_Automated` == `"Yes"`).
3.  **Identify the Bottleneck:** The critical bottleneck is identified by taking the group with automated operations and finding how many **fail** to integrate those automated machines with their digital software systems (where `Q12_Machines_Integrated` == `"No"`).
4.  **Report Findings:** It outputs the total number of manufacturing businesses, how many have automated core operations, and how many suffer from this specific integration bottleneck.

## Outputs for Visualization

At the end of the `extract_insights` function, it returns the four filtered sub-dataframes:
*   `msme_df`
*   `siloed_businesses`
*   `desire_to_invest`
*   `manufacturing_df`

These dataframes are returned so they can be passed down into the subsequent `generate_visualizations()` function, which uses them to generate specific charts (like the funnel chart and correlation matrix) based on these extracted narratives.
