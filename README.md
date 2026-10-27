# Ahmed Almufarriji — Data Science & Analytics Portfolio

[![Python checks](https://github.com/AhmedAlmufarriji/data-science-analytics-portfolio/actions/workflows/python-checks.yml/badge.svg)](https://github.com/AhmedAlmufarriji/data-science-analytics-portfolio/actions/workflows/python-checks.yml)

**Data Science graduate | Python • Machine Learning • SQL • Data Visualization • Power BI**

A curated collection of educational projects: hands-on source code, reproducible notebooks, database designs, and business intelligence examples. See my [separate time-series forecasting capstone](https://github.com/AhmedAlmufarriji/time-series-forecasting-capstone).

> **Scope:** Educational assignments and prototypes; not production software or claims of professional client deployment. Raw customer-level sales exports have not been published.

## Navigate by interest

| I'm interested in… | Start with |
| --- | --- |
| **Applied AI and agent systems** | [KASC Crowd Intelligence V2](https://github.com/AhmedAlmufarriji/KASC-Crowd-Intelligence-V2), [AquaSentinel](06-applied-ai/aquasentinel-ai), [ResiliTwin](06-applied-ai/resilitwin-ai), [SANAD voice-agent case study](06-applied-ai/sanad-agent-engineering) |
| **Machine learning and forecasting** | [Workforce forecasting capstone](https://github.com/AhmedAlmufarriji/time-series-forecasting-capstone), [Medical insurance regression](01-machine-learning/medical-insurance-linear-regression) |
| **Data analytics and BI** | [Restaurant tips EDA](02-data-analysis/eda-tips-analysis), [AdventureWorks analytics](05-business-intelligence/powerbi-adventureworks-sales) |
| **SQL and database engineering** | [MySQL schemas and procedures](04-databases/mysql-electronic-library), [MongoDB data modeling](04-databases/mongodb-blog-system) |

Each project documents its technology, data assumptions, and whether it represents a runnable demo, course exercise, or independent prototype.

## Start here — selected projects

| Project | What you can verify |
|---|---|
| [KASC Crowd Intelligence V2 — Independent Prototype](https://github.com/AhmedAlmufarriji/KASC-Crowd-Intelligence-V2) | Synthetic event-level congestion forecasting, API-driven bilingual dashboard, tested Dijkstra routing, and computed staffing scenarios |
| [AquaSentinel AI — Agentic Water Digital Twin](06-applied-ai/aquasentinel-ai) | Unsupervised leak detection, topology-based localization, demand forecasting, what-if simulation, FastAPI dashboard and an evidence-grounded investigation agent |
| [SANAD — Saudi Arabic Voice Agent Engineering](06-applied-ai/sanad-agent-engineering) | Safety-first insurance conversation design, a scripted Arabic demo, prompt-only bank outage recovery, and three evidence-based call-quality reviews |
| [ResiliTwin AI — Supply Chain Digital Twin](06-applied-ai/resilitwin-ai) | End-to-end ML demand forecasting, risk-aware supplier optimization, Monte Carlo disruption simulations, FastAPI dashboard, and cited evidence search |
| [Workforce Demand Forecasting Capstone](https://github.com/AhmedAlmufarriji/time-series-forecasting-capstone) | Structural-break forecasting, expanding/rolling backtesting, classical models, LightGBM and uncertainty estimates |
| [Medical Insurance Cost Prediction](01-machine-learning/medical-insurance-linear-regression) | 70/30 train-test split, regression evaluation and an executable notebook |
| [Restaurant Tips EDA](02-data-analysis/eda-tips-analysis) | Six charts with univariate, bivariate and multivariate analysis |
| [AdventureWorks Sales Model](05-business-intelligence/powerbi-adventureworks-sales) | Star-schema relationships, Power Query transformations and DAX measures |
| [SQL Electronic Library](04-databases/mysql-electronic-library) | SQL design, foreign keys and borrowing/return procedures |
| [Retail Satisfaction Analysis](05-business-intelligence/powerbi-store-satisfaction) | DAX revenue/profit/customer metrics and data-model documentation |

## Run and verify

```bash
git clone https://github.com/AhmedAlmufarriji/data-science-analytics-portfolio.git
cd data-science-analytics-portfolio
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

For individual Python projects, install their local `requirements.txt` and run the source file or open the included `.ipynb` notebook. SQL and MongoDB projects need their respective database engines. Power BI examples provide reconstruction materials, **not native `.pbix` files**.

## Project index

| Project | Technologies | Focus |
|---|---|---|
| [Medical Insurance Cost Prediction](01-machine-learning/medical-insurance-linear-regression) | Python, pandas, NumPy, scikit-learn, Matplotlib, Seaborn | Explore insurance charges and train/evaluate a multivariate Linear Regression model with a 70/30 train–test split. |
| [Exploratory Data Analysis: Restaurant Tips](02-data-analysis/eda-tips-analysis) | Python, pandas, NumPy, Matplotlib, Seaborn | Univariate, bivariate, and multivariate exploratory data analysis with six visualizations and two insights per plot. |
| [Seaborn Tips: Histogram, Displot and ECDF](02-data-analysis/seaborn-tips-visualizations) | Python, pandas, Matplotlib, Seaborn | Show distribution visualizations by day, sex, and time using Seaborn styles and plot options. |
| [NumPy Arrays and Matrix Operations](02-data-analysis/numpy-array-exercises) | Python, NumPy | Practice linspace, multidimensional arrays, indexing, type conversion, reshaping, stacking and splitting. |
| [Pandas DataFrames and Cleaning](02-data-analysis/pandas-dataframe-cleaning) | Python, pandas, NumPy | Create and inspect a course catalog DataFrame, cast numeric types, preview rows and remove missing values. |
| [People Age Analyzer](03-python/people-age-analyzer) | Python standard library | Validate date-of-birth inputs, calculate age and weekday of birth, compare oldest/youngest and apply sequence operations. |
| [Bank Account with OOP](03-python/bank-account-oop) | Python standard library | An educational bank account simulator with deposits, withdrawals, receipts, encapsulation, and polymorphism. |
| [Bike Factory: Encapsulation in Python](03-python/bike-factory-oop) | Python standard library | Refactor procedural bike inventory logic into a Bike class with state-dependent sale-price updates. |
| [School Management Database (SQL Levels 1–3)](04-databases/mysql-school-management) | MySQL 8, SQL | School database design, data manipulation, analytics, relationships, stored procedures, views and indexes. |
| [Social Network Database (Twitter Simulation)](04-databases/mysql-social-network) | MySQL 8, SQL | Relational design for users, profiles, follows, posts and likes, with foreign keys and stored procedures. |
| [Electronic Library Management Database](04-databases/mysql-electronic-library) | MySQL 8, SQL | Four-stage database design with ER model, book/author/member/borrowings data and lending/return procedures. |
| [MongoDB Blog System](04-databases/mongodb-blog-system) | MongoDB, mongosh, JavaScript | Create a MongoDB blog with users, embedded post comments, follows, plus updates and deletions. |
| [AdventureWorks Sales Analytics (Power BI Companion)](05-business-intelligence/powerbi-adventureworks-sales) | Power BI, Power Query M, DAX, Python, HTML | Data modeling, ETL transformations, DAX KPIs, visualizations and an HTML dashboard for the supplied educational sales dataset. |
| [Retail Sales and Customer Satisfaction Analytics](05-business-intelligence/powerbi-store-satisfaction) | Power BI, DAX, Power Query M, HTML | Model invoices, customers, products and feedback; analyze revenue, gross profit, satisfaction and potential drivers. |
| [AquaSentinel AI — Agentic Water Digital Twin](06-applied-ai/aquasentinel-ai) | Python, scikit-learn, NetworkX, FastAPI, SQLite, SVG | Explainable graph intelligence, sequential ML forecasting, scenario simulation, agent orchestration and local evidence retrieval. |
| [SANAD — Saudi Arabic Agent Engineering](06-applied-ai/sanad-agent-engineering) | HTML, JavaScript, system prompting, voice UX, incident response | An independent Sarj AI assessment case study: knowledge-grounded Najm guidance, prompt-only balance tool fallback, and real-call QA review. |
| [ResiliTwin AI — Supply Chain Resilience](06-applied-ai/resilitwin-ai) | Python, scikit-learn, SciPy LP, FastAPI, JavaScript, Monte Carlo | Reproducible end-to-end decision intelligence and explainable scenario optimization with synthetic data. |

## Technical coverage

**Python:** NumPy, pandas, OOP, validation, date processing.  
**Agent engineering:** Prompt design, Arabic voice UX, safety routing, knowledge grounding, error recovery and conversation QA.  
**Analytics and ML:** EDA, visualization, scikit-learn regression and evaluation.  
**Data systems:** SQL, schema design, stored procedures, MongoDB modeling.  
**Business intelligence:** Power Query, DAX, analytical data modeling and dashboard concepts.

[Explore architecture diagrams for the BI and SQL projects](docs/ARCHITECTURE.md)

## Quality and provenance

- [Automated Python tests](tests/test_portfolio.py) run through [GitHub Actions](.github/workflows/python-checks.yml).
- [Dataset and privacy guidance](DATA_SHARING.md) explains why customer-level source exports are omitted.
- Some interactive HTML dashboards were developed separately from Power BI; they should not be presented as PBIX exports.
- The learning projects use demonstration data and do not constitute production system certifications.

## Repository guidelines

[Contributing](CONTRIBUTING.md) · [Security policy](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Data-sharing and privacy](DATA_SHARING.md) · [Accessibility](ACCESSIBILITY.md) · [Support](SUPPORT.md)

This public repository does not currently include a blanket reuse license; please review ownership and permissions before reusing code or documentation.

[My GitHub profile](https://github.com/AhmedAlmufarriji)
