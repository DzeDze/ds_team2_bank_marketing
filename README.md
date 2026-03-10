# 📊 Bank Marketing Campaign Analysis


## Data Science Institute - Cohort 8 - DS Team 2 - Final Project
<p align="left">
<a href="https://dsteam2bankmarketing-omztqumgpewsyphbyksupa.streamlit.app">
<img src="https://img.shields.io/badge/Live%20Demo-Open%20Streamlit%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
</a>

<br>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python"/>
</a>

<a href="https://github.com/streamlit/streamlit">
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit"/>
</a>

<a href="https://github.com/pandas-dev/pandas">
<img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas"/>
</a>

<a href="https://github.com/scikit-learn/scikit-learn">
<img src="https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikitlearn"/>
</a>

<a href="https://github.com/plotly/plotly.py">
<img src="https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly"/>
</a>
</p>

This project analyzes the [UCI Bank Marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing) dataset to identify the factors that influence whether a customer subscribes to a term deposit and to help optimize future marketing campaigns through data-driven targeting strategies.

The analysis combines **exploratory data analysis, customer segmentation, and predictive modeling** to help marketing teams prioritize high-probability customers, reduce unnecessary outreach, and improve campaign efficiency.

Dataset source:

UCI Machine Learning Repository - Bank Marketing Dataset
[https://archive.ics.uci.edu/dataset/222/bank+marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing)

## Members
- Vinh-phuc (Vince) Nguyen
- Cookiejars8
- Kateryna Makieieva
- Kerensa-wong
- Lanlan Li

## Table of Contents
  
  - [Purpose \& Overview](#purpose--overview)
	  - [Goals \& Objectives](#goals--objectives)
	  - [Target Audience and Stakeholders](#target-audience-and-stakeholders)

- [Dataset](#dataset)

- [Key Business Questions](#key-business-questions)

- [Methodology](#methodology)

- [Project Workflow](#project-workflow)

- [Technical Stack](#technical-stack)

- [Project Structure](#project-structure)

- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Install dependencies](#install-dependencies)
  - [Run the Data Processing \& Model Training Pipelines](#run-the-data-processing--model-training-pipelines)
  - [Launch Streamlit dashboard](#launch-streamlit-dashboard)

- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [1. Customer Demographics](#1-customer-demographics)
  - [2. Financial Profile](#2-financial-profile)
  - [3. Campaign and Previous Contact Behavior](#3-campaign-and-previous-contact-behavior)
  - [4. Customer Segmentation Analysis](#4-customer-segmentation-analysis)
  - [5. Summary of EDA Insights](#5-summary-of-eda-insights)
  - [6. Recommendations](#6-recommendations)

- [Risks \& Unknowns](#risks--unknowns)

- [Conclusion](#conclusion)

- [Limitations \& Future Work](#limitations--future-work)

- [Team Videos](#team-videos)

 <!--- [Additional Guide_Project Setup](#project-structure)-->

## Purpose & Overview
Banks rely heavily on **outbound marketing campaigns**, particularly phone calls, to promote financial products such as term deposits. However, these campaigns typically produce **low conversion rates despite significant operational effort.**

The dataset used in this project reflects this challenge:

- Most contacted customers decline the offer

- Campaigns often involve multiple repeated calls

- Campaign effectiveness varies significantly across customer segments

These issues lead to:

- High operational costs

- Customer fatigue due to repeated outreach

- Inefficient allocation of marketing resources

This project aims to address these problems by identifying **which customers are most likely to subscribe**, allowing marketing teams to move from **high-volume outreach to targeted, data-driven campaigns**.

### Goals & Objectives

The main objective of this project is to improve the effectiveness of direct marketing campaigns by leveraging data analysis and machine learning.

Key goals include:

- Identify customer characteristics associated with higher subscription probability

- Improve marketing targeting precision

- Reduce unnecessary repeated contacts

- Increase campaign conversion rates

- Provide actionable insights for future marketing strategies

### Target Audience and Stakeholders

The findings of this analysis are relevant to several stakeholders involved in marketing strategy, customer analytics, and business decision-making within financial institutions.

* **Marketing Teams** - Use segmentation insights and customer probability rankings to prioritize outreach toward high-potential customers and improve campaign conversion rates.

* **Customer Strategy and CRM Teams** - Leverage customer behavior insights to refine customer segmentation, targeting strategies, and customer relationship management initiatives.
 
* **Business Strategy and Analytics Teams** - Evaluate how customer characteristics and campaign factors influence subscription behavior in order to design more efficient marketing strategies.
 
* **Campaign Operations Teams** - Optimize campaign execution by focusing outreach efforts on customers with higher predicted likelihood of subscription and avoiding low-probability segments.
 
* **Executive Leadership** - Use data-driven insights to guide strategic decisions on marketing investment, customer acquisition strategy, and campaign efficiency.

These insights help support a data-driven marketing approach that improves targeting precision, campaign efficiency, and return on marketing investment.

## Dataset

We use the **Bank Marketing dataset**, which contains information from direct marketing campaigns conducted by a Portuguese banking institution between **May 2008 and November 2010**.

The campaigns were conducted via **phone calls**, with the objective of convincing customers to subscribe to a **term deposit product**.

### **Dataset Details**

- **Records:** 45,211 observations

- **Features:** 16 input variables

- **Target variable:** `y` - whether the client subscribed to a term deposit (`yes` / `no`)

The dataset includes several categories of variables:

### **Customer Demographics**

* age

* job

* marital status

* education

### **Financial Information**

* housing loan status

* personal loan status

* credit default

### **Campaign Information**

* contact method

* number of contacts during campaign
 
* previous campaign outcomes
 
* month and day of contact

### **Target Variable**

* `y`: subscription to a term deposit (`yes` / `no`)

Smaller dataset variants are also available:

| Dataset | Size | Description |
|--------|------|-------------|
| `bank-additional-full.csv` | 41,188 rows | Full dataset with 20 features|
| `bank-additional.csv` | 4,119 rows | 10% sample |
| `bank-full.csv` | 45,211 rows | Older version of the dataset with 17 features |
| `bank.csv` | 4,521 rows | 10% sample of the older dataset version |

For this project we focus primarily on:
`bank-full.csv`

## Key Business Questions

The analysis is guided by several business questions related to **customer demographics, financial characteristics, campaign strategy, and customer segmentation**.

### Customer Demographics
- Which age groups are most likely to subscribe to a term deposit?
- Are retired customers more likely to subscribe than working professionals?
- Does education level influence subscription probability?
- How does marital status affect subscription behavior?

### Financial Profile
- Does higher account balance increase likelihood of subscription?
- Does having a housing loan affect subscription probability?
- Does having a personal loan influence customer decisions?
- Does having credit in default reduce subscription probability?
- Is there an interaction between balance and loan status?

### Campaign Strategy
- Does contact method (cellular vs telephone) influence campaign success?
- Is there an optimal number of contacts in a campaign?
- Does subscription probability decrease after too many calls?
- Which months are associated with higher or lower subscription success?

### Customer Segmentation & Predictive Targeting
- What combinations of customer characteristics yield the highest conversion rates?
- Can we identify **low-probability segments** that should be avoided in future campaigns?
- Do combinations of variables (e.g., loan status + balance) provide stronger insights than single-variable analysis?
- Can customers be **ranked by likelihood of subscription** using predictive models?
- Does combining segmentation analysis with predictive modeling improve targeting effectiveness?
- How can **segmentation insights and predictive models work together** to guide marketing decisions?

These questions help identify which customer groups should be prioritized or avoided in future campaigns.

## Methodology

The project follows a structured workflow to prepare the dataset, analyze customer segments, and develop a predictive ranking model for marketing targeting.

### 1. Data Cleaning and Preparation
The raw dataset was first cleaned to ensure consistency and reliability for analysis.

Key steps include:

- Handling categorical values and ensuring consistent labeling
- Identifying and reviewing variables containing `"unknown"` values
- Removing or adjusting problematic values where necessary
- Converting the target variable `y` into a **binary outcome** representing whether a customer subscribed to a term deposit (`yes` = 1, `no` = 0)

These steps ensure that the dataset is suitable for both segmentation analysis and predictive modeling.

### 2. Feature Transformation (Discretization)
To support clearer segmentation analysis and reduce the influence of extreme values, selected continuous variables were discretized into meaningful buckets.

Specifically:

- **Age** was grouped into age ranges
- **Account balance** was divided into balance buckets (e.g., quartiles)

This transformation allows the analysis to focus on **customer segments rather than individual values**, making patterns easier to interpret and more actionable for marketing decisions.

### 3. Segmentation Analysis
Segmentation analysis was used to explore how combinations of customer characteristics influence subscription behavior.

The analysis focuses on:

- Two-variable combinations (e.g., housing loan × balance group)
- Identifying **high-conversion and low-conversion customer segments**

This step helps reveal which groups of customers are most promising for targeted campaigns.

### 4. Predictive Modeling
A **Logistic Regression model** was implemented to estimate the probability that a customer will subscribe to a term deposit.

Logistic regression was selected because it:

- Produces **probability estimates**
- Allows customers to be **ranked by likelihood of subscription**
- Provides interpretable relationships between variables and the target outcome

Rather than focusing solely on classification accuracy, the model is used primarily as a **ranking tool** to identify high-probability customers for marketing outreach.

### 5. Visualization and Reporting
Insights from both segmentation analysis and predictive modeling are communicated through interactive visualizations.

A **Streamlit dashboard** was developed to:

- Display segmentation results
- Highlight high-performing and low-performing customer segments
- Present decision tables and model-based rankings
- Provide an accessible interface for exploring campaign targeting insights

This interactive reporting approach allows stakeholders to easily interpret the results and apply them to marketing strategy.

## Technical Stack

The project was developed using Python and a set of libraries commonly used in data science workflows.

### Programming Language
- Python

### Data Analysis and Processing
- **pandas** - data manipulation and preprocessing  
- **numpy** - numerical computations

### Machine Learning
- **scikit-learn** - logistic regression modeling and evaluation

### Visualization
- **matplotlib** - statistical visualization
- **seaborn** - enhanced data visualization
- **plotly** - interactive visualizations used in the Streamlit dashboard

### Reporting and Dashboard
- **Streamlit** - interactive dashboard for presenting segmentation insights and model outputs

### Development Environment
- Jupyter Notebooks - exploratory analysis and modeling
- Python scripts (`.py`) - reusable pipelines for data downloading, data processing, feature preparation, and modeling 
- GitHub - version control and collaboration

## Project Structure

```text
DS_TEAM2_BANK_MARKETING/
│
├── data/
│   ├── raw/                     # immutable source datasets
│   │   ├── bank-additional-full.csv
│   │   └── bank-full.csv
│   ├── processed/               # cleaned & feature-engineered outputs
│   └── demo/                    # small demo datasets for testing
│
├── notebooks/                   # exploratory analysis notebooks
│   ├── 00_data_cleaning.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_features_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation_and_explainability.ipynb
│
├── reports/                     # saved figures & visualizations
│
├── artifacts/                   # saved model artifacts and outputs
│
├── app/                         # Streamlit dashboard application
│
├── src/                         # reusable project code
│   ├── pipelines/               # end-to-end pipeline scripts
│   │   ├── download_data.py		# download raw dataset
│   │   ├── process_data.py		# data cleaning and preparation
│   │   ├── export_segmentation.py
│   │   ├── train_models.py		# model training
│   │   └── run_all.py				# run full pipeline
│   │
│   └── utils/                   # helper utilities
│       ├── data_manager.py
│       ├── preprocessing.py
│       ├── transforms.py
│       ├── logger.py
│       └── config.py
│
├── .github/                     # GitHub configuration
├── .gitignore
├── pyproject.toml               # project dependencies & metadata
├── uv.lock                      # dependency lock file
├── project_structure.png        # project architecture diagram
└── README.md                    # project documentation
```
### Structure Design Principles

The project structure follows common **data science and machine learning** repository practices:

* **Data separation**

	Raw data is never modified and processed outputs are stored separately.

* **Notebook vs production code separation**

	Notebooks are used only for exploration, while reusable logic is implemented in `src/`.

* **Pipeline-based workflow**

	The `pipelines` module enables running the entire workflow, from data download to model training through automated scripts.

* **Reproducible environment**

	Dependencies are managed with `uv` via `pyproject.toml` and `uv.lock`.

## Project Setup

### Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies

```bash
# Create virtual environment and install all dependencies from pyproject.toml
uv sync
```

### Run the Data Processing & Model Training Pipelines

This pipeline downloads the dataset, performs data cleaning, preprocessing, and feature engineering, trains the model, and stores all generated artifacts in their respective directories. The outputs are then ready to support reporting and visualization.

```bash
uv run src/pipelines/run_all.py
```

### Launch Streamlit dashboard

Run the following command to start the dashboard locally

```bash
uv run streamlit run app/main.py
```

Alternatively, you can explore the deployed version [here](https://dsteam2bankmarketing-omztqumgpewsyphbyksupa.streamlit.app)

## Exploratory Data Analysis (EDA)

Exploratory Data Analysis (EDA) was conducted to understand how **customer demographics, financial characteristics, and campaign variables influence the likelihood of subscribing to a term deposit**. The goal of this analysis is not only to identify statistical relationships, but also to derive **actionable insights that support marketing targeting decisions.**

The EDA proceeds in four stages:

1. Customer demographics

1. Financial profile 

1. Campaign and previous contact behavior

1. Customer segmentation and predictive ranking

These analyses collectively inform how marketing campaigns can **prioritize high-probability customers and avoid low-yield segments.**

## 1. Customer Demographics

### Age and Subscription Behavior

Age distribution was analyzed to determine whether different age groups exhibit different subscription patterns.

Key observations include:

* Customers aged **65 and above show the highest subscription rates**
 
* Customers aged **26-45 generate a large number of subscribers**, but their conversion rates are relatively moderate
 
* Younger segments such as **18-25 tend to show lower conversion rates**

![](reports/Target_Matrix_by_Age_Group.png)

These results suggest that **age alone does not fully explain subscription behavior**, and that more informative patterns emerge when age is combined with other variables.

### Job Category and Subscription Behavior

Occupation was also evaluated to understand how professional status relates to subscription behavior.

Key findings include:

* **Retired customers show some of the highest conversion rates**

* **Students and unemployed individuals also show relatively strong conversion likelihood**
 
* However, these segments represent **smaller portions of the dataset**

Large occupational groups such as:

* management

* technicians
 
* blue-collar workers
 
* administrative staff

generate the majority of subscribers due to **their larger population sizes**, despite having moderate conversion rates.

This indicates that **small improvements in targeting within these large groups could produce meaningful gains in campaign effectiveness.**

![](reports/Target_Matrix_by_Job_Category.png)

### Age × Job Interaction

To better understand demographic behavior, we analyzed the interaction between age group and occupation.

Several high-performing combinations emerge:

|Job	| Age Group |
|------------|--------------|
|Retired | 56–65, 65+ |
|Student |	18–25 |
|Unemployed |	56–65|

These segments combine **relatively high conversion rates with meaningful segment sizes**, making them potential target groups.

In contrast, large segments such as **blue-ollar workers aged 26-55** show moderate conversion rates but large populations, suggesting potential opportunities for **improved campaign messaging or targeting strategies**.

![](reports/Age_Job_Heatmap.png)

## 2. Financial Profile

Financial characteristics provide some of the strongest indicators of subscription likelihood.

### Account Balance

Account balance shows a strong relationship with subscription behavior.

Key observations:

* Customers with **higher account balances are significantly more likely to subscribe**

* Customers with **low balances show consistently lower conversion rates**

This suggests that **financial capacity is an important driver of willingness to invest in term deposits**.

![](reports/01_balance_vs_subscription_rate.png)

### Housing Loan Status

Housing loan status also influences subscription probability.

Key observations:

* Customers with **housing loans show lower subscription rates**

* Customers **without housing loans are significantly more likely to subscribe**

Housing loans likely represent a **financial commitment that reduces customers' willingness to allocate funds toward savings products.**

![](reports/02_housing_vs_subscription.png)

### Personal Loans

Customers with **personal loans** also exhibit lower subscription probabilities compared with those without personal loans.

This reinforces the idea that **existing debt obligations influence financial decision-making**.

![](reports/03_personal_loan_vs_subscription.png)

### Credit Default Status

Customers with **credit in default** show extremely low subscription rates.

This segment represents a clear **low-priority group for marketing outreach**.

![](reports/04_default_vs_subscription.png)

### Balance and Loan Interaction

When balance is combined with loan status, patterns become clearer.

The strongest conversion rates appear among customers who:

* **have high balances**

* **do not carry housing loans**

This combination represents one of the **most promising financial profiles for targeting term deposit offers**.

![](reports/05_balance_loan_interaction.png)

## 3. Campaign and Previous Contact Behavior

### Seasonal Patterns

Campaign performance varies across months.

Key observations:

* **March shows the highest subscription rates**
 
* **September, October, and December** also show relatively strong performance
 
* Other months show moderate or lower success rates

This suggests that **seasonality may influence customer responsiveness to marketing campaigns.**

![](reports/subscription_rate_by_month.png)

### Call Duration

Call duration shows a strong correlation with subscription success.

Longer calls are more likely to result in successful subscriptions. However, this variable cannot be used in predictive targeting because **call duration is only known after the call occurs**, making it a **data leakage variable**.

Therefore, it is used only for **behavioral interpretation rather than predictive modeling**.

![](reports/subscription_rate_by_call_duration.png)

### Previous Campaign Outcome

Previous campaign outcomes provide one of the strongest predictors of subscription behavior.

Key findings include:

* Customers with **previous campaign success show dramatically higher subscription rates**

* Customers with **previous failures show much lower conversion probabilities**

This suggests that **retargeting previously successful customers may be highly effective.**

![](reports/subscription_rate_by_previous_campaign.png)

### Recency of Contact

The variable **pdays** measures the number of days since the last contact.

Key observation:

* Customers contacted **more recently show higher subscription probabilities**

* Conversion rates decline as the **time since last contact increases**

This highlights the importance of **recency in marketing engagement**.

![](reports/04_pdays_vs_subscription.png)

## 4. Customer Segmentation Analysis

Two-way segmentation analysis evaluates pairs of variables simultaneously, allowing us to identify:

* high-value target segments

* low-probability segments to avoid

### Top Target Segments

The **Top Target Segments** analysis identifies combinations of characteristics with **conversion rates significantly above the overall dataset average (11.7%)**.

Typical high-performing segments include:

* Customers **without housing loans and with high balances**

* Older customers **without major financial obligations**
 
* Customers with **strong financial profiles and favorable past campaign interactions**

These segments represent the **most promising customers for marketing outreach.**

![](reports/top_target_segments.png)

This visualization ranks segments by conversion rate and lift, helping marketers identify the most valuable customer groups.

### Segments to Avoid

The **Segments to Avoid** analysis highlights groups that consistently show very low subscription probabilities.

Typical low-performing segments include:

* Customers **with housing loans and low balances**

* Customers **with multiple financial obligations**
 
* Segments **with weak financial profiles**

Targeting these groups is unlikely to generate meaningful results and may reduce campaign efficiency.

Avoiding these segments allows marketing teams to:

* reduce unnecessary outreach

* improve campaign ROI
 
* allocate resources more effectively

![](reports/segments_to_avoid.png)

### Decision Table

To translate segmentation insights into actionable guidance, a decision table was created summarizing key segments and their marketing implications. This table provides a **clear operational guide for campaign targeting.**

![](reports/decision_table.png)

## 5. Summary of EDA Insights

* Older customers and retired segments show relatively higher subscription rates, though large working-age groups still account for most subscribers due to their population size.
 
* Financial profile is a strong indicator of subscription behavior. Customers with higher account balances are significantly more likely to subscribe, while customers with housing loans, personal loans, or credit default indicators show lower conversion rates.
 
* Previous campaign outcomes strongly influence future behavior. Customers who previously responded successfully to campaigns have much higher subscription probabilities.
 
* Two-way segmentation analysis helps identify meaningful customer groups, revealing segments with consistently high or low conversion rates.
 
* Segmentation highlights high-potential target segments (e.g., financially stronger customers without loan obligations) and low-probability segments that are less suitable for marketing outreach.
 
* Logistic regression enables customer-level probability ranking, allowing campaigns to prioritize customers most likely to subscribe.

## 6. Recommendations

* **Prioritize customers with stronger financial profiles**, particularly those with higher balances and fewer loan obligations.
 
* **Reduce outreach to low-probability segments**, such as customers with housing loans and low balances.
 
* **Retarget customers with previous successful campaign interactions**, as they show higher likelihood of subscribing again.
 
* **Use logistic regression ranking to prioritize outreach**, focusing marketing resources on the customers most likely to convert.

## Risks & Unknowns

This project includes several limitations that may affect the interpretation or real-world application of results.

### Risks
**Class Imbalance & Model Bias**

The dataset is heavily skewed toward customers who **did not subscribe**. This imbalance may cause models to favor predicting "no," reducing their ability to identify potential subscribers.

**Limited Generalizability**

The dataset originates from a **Portuguese bank**, and customer behavior, regulations, and financial habits may differ in other markets such as **Canada**.

**Outdated Data**

The data was collected before **2013**, and changes in customer expectations, economic conditions, and marketing channels may affect the relevance of findings today.

**Data Quality Issues**

Some fields contain **"unknown" values or unclear categories**, which may weaken interpretability and model performance.

**Outliers**

Extreme values in variables such as **account balance or call duration** may distort the analysis.

**Missing Important Variables**

Important behavioral drivers are not included in the dataset, such as:

* income
* digital engagement 
* geographic location
* psychological motivations

**Model Transferability**

A model trained on historical campaigns may not perform equally well on **new campaigns with different scripts or strategies.**

**Ethical & Consent Considerations**

It is unclear whether customers consented to repeated outreach, and predictive targeting may risk reinforcing **existing biases in historical data.**

**Correlation vs Causation**

Observed relationships represent a**ssociations rather than causal effects**, meaning the dataset cannot fully explain *why* customers subscribe.

### Unknowns

Several key business factors are not captured in the dataset.

**Campaign Costs & Profitability**

We do not know:

* the cost of each campaign
* the profit generated by successful subscriptions

This prevents accurate **ROI estimation**.

**Customer Motivations**

The dataset does not explain **why customers declined or accepted the offer**, limiting the ability to design improved messaging.

**Behavioral Context**

Important contextual factors such as:

* digital activity
* geographic location
* lifestyle characteristics

are not available.

**Customer Lifetime Value**

The dataset does not indicate:

* how long customers kept their term deposits
* long-term profitability of subscribers

**Loan Usage Details**

The dataset indicates whether a customer has a loan but does not show **how actively the loan is used**, which may influence financial behavior.

**Campaign Strategy Changes**

Information about **call scripts, targeting rules, and marketing strategies** is not included.

**External Economic Conditions**

Macroeconomic events that could influence financial decisions are not captured.

**Contact Timing**

The dataset does not include the **time of day customers were contacted**, which may affect response rates.


## Conclusion

This project demonstrates how data analysis and machine learning can support more effective marketing targeting for term deposit campaigns. Using the UCI Bank Marketing dataset, we combined **exploratory analysis, customer segmentation, and predictive modeling** to identify the factors that influence subscription behavior.

The analysis highlights that customers with **stronger financial profiles, fewer loan obligations, and positive previous campaign outcomes** are more likely to subscribe. Two-way segmentation helps identify **high-potential target segments and low-probability segments**, while logistic regression enables **customer-level probability ranking** to prioritize outreach.

Together, these approaches support a shift from **broad, high-volume outreach toward more targeted and data-driven marketing strategies**, helping improve campaign efficiency and reduce unnecessary contacts. The results are presented through an **interactive Streamlit dashboard**, which allows stakeholders to explore segmentation insights and model outputs in a user-friendly way.

## Limitations & Future Work

While this project provides useful insights for marketing targeting, several opportunities exist to improve and extend the analysis.

- **Model improvement** - The current implementation uses logistic regression for interpretability and customer ranking. Future work could explore more advanced models such as **Random Forest, Gradient Boosting (XGBoost/LightGBM)**, or **Neural Networks** to capture more complex patterns in customer behavior.

- **Class imbalance handling** - Because the dataset contains far fewer subscribers than non-subscribers, future work could apply techniques such as **SMOTE**, **undersampling, or precision-recall optimization** to improve the model’s ability to identify potential subscribers.

- **Richer data features** - Additional variables such as **income, geographic information, digital engagement behavior, or customer lifetime value** could improve predictive performance and enable deeper segmentation insights.

- **Lightweight CI/CD integration** - Future work could include adding **simple CI pipelines** (e.g., GitHub Actions) to **automatically test data pipelines, validate model training, and ensure the Streamlit dashboard** continues to run after code updates.

These improvements would help transform the current analysis into a more scalable marketing analytics system capable of supporting continuous campaign optimization.

# Team Videos
 | Name | Links |
 | --- | --- |
 | Vinh-phuc (Vince) Nguyen | [Video Link](https://drive.google.com/file/d/1vOWN-QcuqwxCfk-j6LtCNiNw64hCOVs3/view) |
 | Cookiejars8 | [Video Link](https://drive.google.com/drive/folders/1ZMKaL5Wt-paKmv6_XxYwoKOefxINcQXF) |
 | Kateryna Makieieva | [Video Link](https://drive.google.com/file/d/1DHBxbKdbTPz_CL6w-p0iqL5dLxmBBqwH/view?usp=sharing)|
 | kerensa-wong | [Video Link](https://drive.google.com/file/d/1vvHW3TirXDJPbQQtiiN9TbBgZ8cSanOX/view?usp=drive_link)| 
 | Lanlan Li | [Video Link](https://drive.google.com/file/d/1jXimNCQlhScW2aPokX7pAl6hKu8LPDEE/view?usp=sharing) |


## Credits

* Team: DS Team 2 - University of Toronto, Data Sciences Institute
* Dataset: UC Irvine Machine Learning Repository
* Contributors: All team members
