# Data-Analyst-Portfolio
# Comprehensive Data Analytics & Engineering Portfolio

Welcome to my technical data portfolio. This repository serves as an end-to-end showcase of production-ready systems, encompassing modular ETL data pipelines, relational data modeling (Star Schemas), advanced SQL analysis, and interactive DirectQuery business intelligence dashboards.

## Portfolio Directory Architecture

### [Ecommerce-Sales-Analytics](./02_Ecommerce-Sales-Analytics)
*   **Core Focus:** Relational Database Analytics & Executive Dashboard Engineering
*   **Technologies:** PostgreSQL, Power BI, Advanced SQL
*   **Key Implementations:** Implemented a multi-table database schema in a PostgreSQL backend. Developed advanced queries incorporating Common Table Expressions (CTEs) and analytical Window Functions (`LAG`) to compute Month-over-Month (MoM) corporate growth vectors. Designed an executive performance dashboard in Power BI leveraging a live `DirectQuery` data gateway to expose product revenue trends and regional distribution efficiency metrics.

### [Automated-Market-Pipeline](./03_Automated-Market-Pipeline)
*   **Core Focus:** Automated Data Collection & Ingestion Infrastructure
*   **Technologies:** Python 3, Pandas, SQLAlchemy, PostgreSQL
*   **Key Implementations:** Built a modular Python Extract-Transform-Load (ETL) utility script. Configured structured transformation logic via Pandas to enforce quality gates (null filtering, structural alignment). Implemented an atomic database insertion engine powered by SQLAlchemy staging configurations and custom `UPSERT` logic (`ON CONFLICT DO UPDATE`) to guarantee data storage integrity on primary key constraints.

### [Predictive-Maintenance-Pipeline](./04_Predictive-Maintenance-Pipeline)
*   **Core Focus:** Real-Time Stream Simulation & Rule-Based Machine Learning Alerts
*   **Technologies:** Python, Scikit-Learn (Threshold Logic), Anaconda, PostgreSQL
*   **Key Implementations:** Engineered an automated data streaming environment tracking industrial mechanical sensor variables (Temperature, Vibration velocity, RPM speed). Integrated a decision mapping classification module mimicking a Random Forest model to calculate machine health probability scores. The engine isolates anomalies and appends warning signals cleanly into an enterprise database layout.

### [Healthcare-Operational-Analytics](./05_Healthcare-Operational-Analytics)
*   **Core Focus:** Clinical Triage Operational Tracking & Live Monitoring
*   **Technologies:** Python, Pandas, Power BI Desktop (DirectQuery), PostgreSQL
*   **Key Implementations:** Developed an emergency room admission logging stream tracking patient turnaround latencies. Linked the streaming database backend directly into Power BI to build an interactive, live-updating monitoring canvas mapping clinical department throughput, urgency weights, and billing performance metrics.

---
### Technical Summary Grouping
*   **Languages:** SQL (PostgreSQL, MySQL), Python (Pandas, NumPy, SQLAlchemy, Scikit-Learn)
*   **BI & Analytics:** Power BI Desktop (Power Query, DAX, DirectQuery), Tableau Public, Excel
*   **Education Background:** B.Tech in Data Science, Class of 2026 (Savitribai Phule Pune University)

*Developed by Aman Ganesh Kanojia. Connect with me on [LinkedIn](https://linkedin.com) to discuss data analytics opportunities.*
