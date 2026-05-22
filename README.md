# 🌍 Global Data Salaries

---

## 📌 Project Use Case
In today's rapidly evolving tech landscape, many organizations face significant talent acquisition hurdles, often experiencing high candidate rejection rates due to salary offerings that do not align with current market benchmarks. Conversely, data professionals and job seekers struggle to accurately gauge their market value and understand what compensation they truly deserve. 

**The core objective of this project** is to bridge this gap. By developing an automated data engineering ecosystem and a predictive machine learning model, this project provides data-driven salary insights in **Saudi Riyals (SAR)** to help both employers and professionals make informed, market-aligned compensation decisions.

---

## 📌 Data Overview
The project utilizes a comprehensive global dataset containing over **93,000 records** and **11 key features** reflecting modern data science and engineering roles.

* **Data Source:** [Kaggle - Latest Data Science Job Salaries Dataset](https://www.kaggle.com/datasets/saurabhbadole/latest-data-science-job-salaries-2024)

### Dataset Features Schema:
| Feature Name | Description |
| :--- | :--- |
| `work_year` | The specific year the salary data was recorded. |
| `experience_level` | The employee's professional experience level (e.g., Entry-level, Mid-level, Senior, Executive). |
| `employment_type` | The type of employment contract (Full-time, Part-time, Contract, Freelance). |
| `job_title` | The specific role or title of the employee within the data ecosystem. |
| `salary` | The gross salary amount in its original currency. |
| `salary_currency` | The currency in which the salary was originally paid (e.g., USD, EUR, GBP). |
| `salary_in_usd` | The standardized salary amount converted into US Dollars for global comparison. |
| `employee_residence` | The primary country of residence of the employee. |
| `remote_ratio` | The proportion of remote work allowed for the position (0%, 50%, or 100%). |
| `company_location` | The country where the employing company's office is located. |
| `company_size` | The organizational size based on employee count (Small, Medium, Large). |

---
---

## 🏗️ Technical Architecture & Outlines

### 1. Data Ingestion (Google Cloud Storage)
- **Data Landing Zone:** The raw global dataset (`Latest_Data_Science_Job_Salaries_2024.csv`) was securely uploaded and stored in **Google Cloud Storage (GCS)** buckets (`gs://salary_data_qatar_bucket`), serving as the initial immutable landing layer.
![Dataflow Pipeline](dataflow_pipeline.png)

### 2. Data Exploration & Staging (Google BigQuery)
Before setting up automated orchestration, the raw data was loaded directly into **Google BigQuery** (`salary_data_set.global_salaries`) to establish a staging environment.
- **Data Profiling & Inspection:** BigQuery was utilized to visually inspect value distributions, assess structural variations, and theoretically analyze what specific data cleaning and mapping logic the dataset required (without generating visual dashboard charts at this stage).
- **The Core Strategy (Automation vs. Manual Tasks):** While BigQuery possesses massive processing power to perform manual SQL alterations, the main goal of this project was to achieve **complete, production-ready pipeline automation**. Therefore, the data transformation rules were decoupled from manual queries and written entirely into an automated execution block.

### 3. Automated ETL Pipeline (Google Cloud Dataflow)
To bridge the staging and final production layers, a resilient and fully automated ETL pipeline was built using the **Apache Beam SDK** and executed on **Google Cloud Dataflow** (`DataflowRunner`) using the `me-central1` Doha region infrastructure.

The automated pipeline performs the following dynamic data engineering steps (`SalaryDataTransform`):
* **Read Operation:** Programmatically streams raw records from the initial BigQuery staging table (`global_salaries`).
* **Currency Conversion & Cleanup:** Automatically converts international standardized figures from USD into **Saudi Riyals (SAR)** (`salary_in_usd * 3.75`) to drive localization for the Saudi market context, while dynamically popping out legacy columns (`salary`, `salary_currency`) to save warehouse compute resources.
* **Feature Standardization Maps:** Maps complex or shorthand alpha-codes into descriptive, user-friendly professional labels for features like `company_size` (S/M/L to Small/Medium/Large), `experience_level` (EN/MI/SE/EX), and `employment_type`.
* **Work Environment Translation:** Evaluates numeric remote workspace ratios to dynamically classify environments into structured groups (`On-site`, `Hybrid`, `Remote`).
* **Advanced Text Classification (Regex Matching):** Implements Regular Expressions (`re.search`) to intelligently scan and group dozens of complex, raw operational titles into 7 clean categorical core tech domains (e.g., *AI & Machine Learning*, *Data Science*, *Data Engineering*, *Data Management & Governance*).
* **Geographic Regional Mapping:** Groups disparate international country codes (`company_location`) into consolidated global economic regions (such as *United States*, *Europe*, and an explicit grouping for the *Middle East & Africa* containing `SA`).
* **Write Operation:** Leverages BigQuery's auto-detect schema functionality to automatically overwrite and load clean, completely transformed records into the production-ready target layer (`global_salaries_cleaned`).

#### 🛠️ Dataflow Execution Graph:
![Dataflow Pipeline](dataflow_pipeline.png)
