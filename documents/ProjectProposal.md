# 📊 Bank Marketing Project – Week 1 - Project Proposal

## 1. Business Problem
Banks rely on outbound phone campaigns to promote term deposits, yet these campaigns often produce low conversion rates despite significant time and resource investment. 
The UCI Bank Marketing dataset reflects this challenge: 
- most customers decline the offer,
- many require repeated contact attempts,
and campaign efficiency varies widely

These issue lead to high operational costs, customer fatigue, and limited return on marketing spend.

The key business problem is **identifying which customers are most likely to subscribe**, enabling the bank to:
- Focus efforts on customers with higher likelihood of conversion
- Reduce wasted outreach and avoid unnecessary repeated calls
- Improve campaign efficiency and resource allocation
- Increase subscription rates for term deposits
- Shift from broad, high-volume calling to targeted, data-driven marketing


## 2. Business Motivation
Banks invest heavily in marketing campaigns, but many contacts do not lead to conversions.  
Our motivation is to:
- Improve targeting precision and campaign efficiency.
- Reduce unnecessary repeated contacts.
- Increase subscription rates for term deposits.
- Provide actionable insights for future marketing strategies.



## 3. Dataset
We are using the [UCI Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing), which contains data from direct marketing campaigns of a Portuguese banking institution.  These campaigns were conducted via phone calls between May 2008 and November 2010.

**Key Details**
- **Size:** 41,188 records with 20 input features (bank-additional-full.csv).  
- **Content:** Customer demographics (age, job, marital status, education), financial attributes (balance, housing loan, personal plan), and campaign details (contact type, month, number of contacts, pervious outcomes).  
- **Target variable:** (`y`) - Whether the client subscribed to a term deposit.

**Other versions avaiable:**
- bank-additional.csv - 10% sample (4,119 records, 20 features)
- bank-full.csv - full dataset with 17 features (older version)
- bank.csv - 10% sample of the older version (17 features)

These smaller datasets are often used for testing computationally demanding algorithms

**Classification Gaol:** Predict whether a customer will subscribe to a term deposit (`yes`)/(`no`)



## 4 Risks & Unknowns

### 4.1 Risks
These factors may affect how reliable our analysis is and how well our model performs in real marketing situations.

- **Class Imbalance & Model Bias:** The dataset is heavily skewed toward "no" subscriptions, which can make accuracy appear high even if the model simply predicts "no" for most customers, reducing the model's ability to correctly identify potential subscribers

- **Limited Generalizability** The dataset comes from a Portuguese bank. Customer behnavior, regulations, and financial habits may differ in other countries, so results may not applicable to markets like Canada

- **Outdated Data:** Data is from before 2013. Customer expectations, economic conditions, and marketing practices have changed since then, which may reduce how relevant the predictions are today

- **Data Quality:** Several fields contain "unknown" values (job, education, contact, poutcome) or unclear categories (such as "other" in putcome). These gaps make it harder to interpret patterns and may weaken model performance

- **Outliers & Unusual Values:** Extremely high balances or very long call durations may distort the analysis and influence the model in unrealistic ways

- **Missing Important Information:** Key factors such as income, digital engagement, geographic location, and personal motivations are not included. Without these, the model may miss important drivers of customer decisions

- **Model Transferability:** Even if a model performs well on historical data, it may struggle with new campaigns that use different scripts, strategies, or customer segments

- **Ethical & Consent Concerns:** It is unclear whether customers agreed to repeated contact. There is also a risk of unintentionally targeting grpus unfairly if the model picks up patterns that reflect bias in the data

- **Correlation is not Causation:** The dataset shows associations, but these do not necessarily explain why customers subscribe. Decisions based solely on correlations may be misleading

### 4.2 Unknowns
Several important business and behavioral factors are not captured in the dataset, which limits our ability to fully understand customer decision-making or estimate the real-world impact of the campaign.

- **Campaign Costs & Profitability:** We do not know how much each market campaign costs or how much each successful subscription generates, making it difficult to estimate return on investment (ROI)

- **Customer Motivations:** The dataset does not explain why customers choose not to subscribe (behavioral, psychological, or contextual reasons), which limits our ability to design better messaging or offers

- **Missing Behavioral & Contextual Factors:** Personal motivations, digital activity, and geographic information are not included, even though they may strongly influence outcome

- **Customer Behavior After Subscribing:** The dataset does not show how long customers keep their term deposits or whether they remain profitable over time. Term-deposit retention influence profitability, customer lifetime value, and overall ROI, so this missing information limits our understanding of long-term impact

- **Loan Usage:** The dataset indicates whether a customer has a loan but does not show whether the loan is actively being used. Loan usage affects financial behavior, risk levels, and cross-sell potential, making this gap important for understand broader customer needs

- **Changes in Campaign Strategy:** The dataset does not include information on call  scripts, targeting rules, or campaign approaches, and it is unclear whether these have changed over time. Shifts in campaign strategy could influence customer responses and affect how well our findings generalize

- **External Economic Conditions:** Broader economic events that may have influenced customer decisions are not captured in the dataset

- **Call Timing & Contact Preferences:** The time of day (morning or evening) customers were contacted is missing, and it is unclear whether they consented to repeated outreach



## 5. Approach to Analysis
- **Exploratory Data Analysis (EDA):** Identify patterns in demographics, financials, and campaign outcomes.  
- **Classification:** Predict whether a customer will subscribe ('yes'/'no') using logistic regression, random forest, and gradient boosting models
    **Goal:** To identify the most powerful predictors of subscription
- **Regression:** Predict continuous outcomes such as call duration or account balance
    **Goal:** Understnd numeric trends that may influence campaign success  
- **Segmentation:** Identify high- and low-probability customer groups for targeted strategies.  
- **Visualization & Explainability:** Use Python libraries (seaborn, matplotlib, Plotly) to communicate insights, and SHAP values for model interpretability.  



## 6. Questions:
**a. Demographics:**
- Which age groups are most likely to subscribe to a term deposit?
- Are retired customers more likely to subscribe than working professionals?
- Does a customer's age and job jointly infuence the probability of subscription?
- Does a customer's education level impact subscription?
- How does marital status impact subscription behavior?

**b. Financial Profile:**
- Does higher account balance increase likelihood of subscription?
- Does having a housing loan affect subscription probability?
- Does having a personal loan affect subscription behavior?
- Does having credit in default reduce subscription probability?
- Is there an interaction between balance and loan status?
- Can subscription likelihood be linked to other products (e.g., loans)?
- How many loans are personal vs housing loans?

**c. Campaign Strategy:**
- Does contact type (cellular vs telephone) affect subscription success?
- Is there an optimal number of contacts in a campaign?
- Does subscription probability decrease after too many calls?
- What months have the highest vs lowest subscription success?
- Are certain days of the week more effective?
- Is there evidence of seasonal patterns in subscription behavior?
- How does call duration relate to subscription?

**d. Previous Campaign Effectiveness:**
- How does the outcome of a previous campaign affect current success?
- Are customers with previous successful campaigns more likely to subscribe again?
- Are customers previously unsuccessful unlikely to convert again?
- Does time since last contact (pdays) influence success probability?
- Are existing customers more likely to subscribe than new ones?

**e. Segmentation & Predictions:**
- What combination of age, job, balance, and loan status yields the highest conversion rate?
- Can we identify low-probability segments to avoid targeting?
- Can customers be ranked by likelihood of subscription?
- Does combining variables provide stronger predictive power than single variables?
- Does the combination of age + job + loan status improve prediction compared to single factors?


## 7. Roles & Tasks 
 - **Vinh-phuc Nguyen:** Repo Administration, Segmentation & Predictions EDA, 
   Visualisation - Streamlit
 - **Cookiejars8:** Financial Profile EDA, Previous Campaign Effectiveness EDA, Slideshow
 - **Kateryna Makieieva:** Data Cleaning, Preprocessing, Handling missing values, Campaign   
   Strategy EDA, Classification Model, Wireframe
 - **kerensa-wong:** Readme file, Project Proposal, Demographics EDA, Explainability (SHAP)
 - Chris Odetola
  - Lanlan Li

- **All Members:** Contribute to documentation, discussion of risks, and presentation of findings.



## Next Steps
- Complete initial EDA and share visual summaries.  
- Begin preprocessing pipeline for categorical and numeric features.  
- Draft first set of visualizations for demographics and campaign outcomes.  
