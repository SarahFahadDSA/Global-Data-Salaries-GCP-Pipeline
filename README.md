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

## 🏗️ Technical Architecture & Outlines

### 1. Data Ingestion (Google Cloud Storage)
- **Data Landing Zone:** The raw global dataset (`DataScience_salaries_2025.csv`) was securely uploaded and stored in **Google Cloud Storage (GCS)** buckets (`salary-data-raw-tuwaiq-bootcamp`), serving as the initial immutable landing layer.
![Google Cloud Storage](Google_Storage_Bucket.png)

### 2. Data Exploration & Staging (Google BigQuery)
Before setting up automated orchestration, the raw data was loaded directly into **Google BigQuery** (`salary_data_set.global_salaries`) to establish a staging environment.
![Google BigQuery](BigQuery.png)
- **Data Profiling & Inspection:** BigQuery was utilized to visually inspect value distributions, assess structural variations, and theoretically analyze what specific data cleaning and mapping logic the dataset required (without generating visual dashboard charts at this stage).
- **The Core Strategy (Automation vs. Manual Tasks):** While BigQuery possesses massive processing power to perform manual SQL alterations, the main goal of this project was to achieve **complete, production-ready pipeline automation**. Therefore, the data transformation rules were decoupled from manual queries and written entirely into an automated execution block.

### 3. Automated ETL Pipeline (Google Cloud Dataflow)
To achieve complete pipeline automation, a production-grade ETL ecosystem was engineered using the **Apache Beam ** and executed via **Google Cloud Dataflow** (`DataflowRunner`) 

The complete codebase for this pipeline can be reviewed here:
👉 [View Apache Beam ETL Pipeline Script](pipeline_process.py)

#### 🛠️ Dataflow Execution Graph:
![Dataflow Pipeline](Pipeline.png)

### 🔄 Execution Flow & Transformations (`SalaryDataTransform`)
Once triggered, the pipeline processes the data step-by-step through an isolated and fault-tolerant execution graph:

#### Step A: Data Ingestion (`Read From BigQuery`)
* Programmatically streams raw operational records directly from the initial Google BigQuery staging table.

#### Step B: Core Processing Logic (`beam.ParDo()`)
Before applying any transformations, the pipeline creates an isolated copy of each streaming record (`element.copy()`) to maintain thread safety and prevent raw data corruption. It then sequentially executes the following business logic:

1. **Currency Conversion & Column Cleanup:** Converts international standardized figures from USD into **Saudi Riyals (SAR)** (`salary_in_usd * 3.75`) to drive localization for the Saudi market context. It then dynamically drops legacy, unneeded source columns (`salary`, `salary_currency`) using Python's `pop()` method to minimize storage overhead.
2. **Company Size Mapping:** Maps complex shorthand alpha-codes into descriptive, user-friendly professional labels (Translates `S`, `M`, `L` into `Small`, `Medium`, `Large`).
3. **Experience Level Mapping:** Standardizes operational status attributes (`EN`, `MI`, `SE`, `EX` into `Entry-level`, `Mid-level`, `Senior-level`, `Executive-level`).
4. **Employment Type Mapping:** Converts contractual shorthand variations (`FT`, `PT`, `CT`, `FL`) into explicit designations (`Full-time`, `Part-time`, `Contract`, `Freelance`).
5. **Remote Work Ratio Mapping:** Evaluates numeric workspace ratios (`remote_ratio`) to dynamically categorize employees into structural work environments (`On-site` for 0, `Hybrid` for 50, and `Remote` for 100).
6. **Advanced Text Classification (Regex Matching):** Implements Regular Expressions (`re.search`) to intelligently scan raw, complex job titles and group them cleanly into 7 core technological domains (e.g., *AI & Machine Learning*, *Data Science*, *Data Engineering*, *Data Analysis & BI*, *Data Management & Governance*, *Software & Cloud Engineering*, and *Product & Business*).
7. **Geographic Regional Mapping:** Groups disparate international country codes (`company_location`) into consolidated global economic regions, explicitly creating a dedicated grouping for the **Middle East & Africa** region (which includes `SA` for Saudi Arabia).

#### Step C: Fault-Tolerant Exception Handling
* The entire analytical block is wrapped inside a robust `try-except` structure. If a corrupted row or data anomaly is encountered, it captures and logs the error specific to that row (`Error processing row: {e}`) while keeping the entire enterprise pipeline running smoothly without crashes.

#### Step D: Warehouse Loading (`Write To BigQuery`)
* Leverages BigQuery's auto-detect schema functionality (`SCHEMA_AUTODETECT`) to automatically infer table schemas, overwriting and loading the clean, completely transformed rows into the target layer (`global_salaries_cleaned`) using `WRITE_TRUNCATE`.

---

### 4. 📊 Interactive Dashboard (Looker Studio)

An interactive business intelligence dashboard was built using **Google Looker Studio**, connecting directly to the cleaned BigQuery table (`global_salaries_cleaned`) as its live data source.

> *Note: The live dashboard has been taken offline as the underlying BigQuery dataset was decommissioned after project completion. Screenshots below reflect the dashboard's full functionality.*


#### 📋 Dashboard Overview
The dashboard provides a comprehensive, filterable view of global data salary benchmarks presented in **Saudi Riyals (SAR)**. It features six dynamic filter controls — `work_year`, `job_category`, `job_title`, `experience_level`, `employment_type`, and `company_size` — allowing users to slice the data from any angle.

**Key KPI cards (unfiltered — all 93,597 records):**
| Metric | Value |
| :--- | :--- |
| Average Annual Salary (SAR) | 590,804 |
| Average Monthly Salary (SAR) | 49,234 |
| Total Records | 93,597 |

![Global Data Salary Dashboard](Dashboard.png)

---

#### 📈 Charts & Insights

**1. Global Average Monthly Salary (2020 – 2025)**

<img src="Global Average Monthly Salary (2020-2025).png" alt="Global Salary Trend" width="100%">

> 💡 **Insight:** The data profession experienced explosive salary growth between 2021 and 2023 — a ~60% increase in just two years — likely driven by the post-pandemic surge in digital transformation and the rapid rise of AI adoption across industries. The plateau observed from 2023 to 2025 suggests the market is maturing, with salaries stabilizing around the 49K–50K SAR range as supply of data talent begins to catch up with demand.

---

**2. Avg. Monthly Salary by Global Region (Interactive Map)**

A bubble map where size corresponds to salary magnitude. Hover over any region to view its exact average monthly salary in SAR.

![Avg. Monthly Salary by Region — US](Avg_Monthly_Salary_by_Region_US.png)
![Avg. Monthly Salary by Region — Middle East](Avg_Monthly_Salary_by_Region_MiddleEast.png)

| Region | Avg. Monthly Salary (SAR) |
| :--- | :--- |
| North America (United States) | 51,078.79 |
| Middle East & Africa | 40,361.69 |

> 💡 **Insight:** North America commands the highest salaries globally, sitting ~4% above the overall average — reinforcing the US as the benchmark market for data compensation. The Middle East & Africa region, at SAR 40,361, trails the global average by ~18%, revealing a significant compensation gap despite the region's growing investment in data and AI infrastructure (particularly relevant in the Saudi context given Vision 2030 initiatives). This gap represents both a challenge for local talent retention and an opportunity for organizations to adjust compensation strategies.

---

**3. Avg. Monthly Salary by Job Category**

![...](Avg_Monthly_Salary_by_Job_Category.png)

| Rank | Job Category | Avg. Monthly Salary (SAR) |
| :--- | :--- | :--- |
| 1 | AI & Machine Learning | 58,400 |
| 2 | Software & Cloud Engineering | 56,600 |
| 3 | Product & Business | 53,200 |
| 4 | Data Science | 51,500 |
| 5 | Other Specializations | 50,000 |
| 6 | Data Engineering | 47,800 |
| 7 | Data Management & Governance | 37,600 |
| 8 | Data Analysis & BI | 34,700 |

> 💡 **Insight:** AI & Machine Learning roles command a 19% premium over the dataset-wide average, reflecting the current scarcity of specialized AI talent and the high business value these roles deliver. Notably, Data Analysis & BI — often considered an entry point into the data field — earns nearly 41% less than AI & ML roles, highlighting a steep compensation ladder within the data profession. Data Engineering sits mid-table, suggesting it is a well-established and commoditized discipline, while the relatively low ranking of Data Management & Governance may indicate that organizations still undervalue data quality and stewardship functions despite their strategic importance.

---

#### 🔍 Dashboard Filtering Example

The following example demonstrates the dashboard's dynamic filtering capability. When filtering by **`job_category: Data Engineering`** and **`job_title: Data Engineer`**, the entire dashboard recalculates to reflect that specific segment:

| Metric | Filtered View (Data Engineer) |
| :--- | :--- |
| Average Annual Salary (SAR) | 556,177 |
| Average Monthly Salary (SAR) | 46,348 |
| Total Records | 11,323 |

> 💡 **Insight:** Data Engineers represent a substantial segment of the dataset (11,323 out of 93,597 records — ~12%), confirming it as one of the most prevalent roles in the data field. Their average monthly salary of SAR 46,348 sits ~6% below the global average, suggesting that while demand is high, the growing availability of Data Engineering talent is tempering compensation growth relative to more specialized categories like AI & ML.

![Dashboard — Filtered: Data Engineer](Dashboard_DE.png)


