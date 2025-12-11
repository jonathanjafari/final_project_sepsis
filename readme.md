# Cloud-Based Sepsis Early Warning Pipeline  
### HHA 504 – Final Project (Cloud Integration Mini-Capstone)

This project presents a small, cloud-oriented design for a sepsis early warning pipeline using synthetic clinical data.  
It also includes an optional Flask prototype demonstrating how a simple web service might interact with cloud resources.  
No PHI is used — all data described is synthetic.

---

## 📁 Repository Contents
```
final_project_sepsis/
│
├── use_case.md              # Problem statement, users, data sources, workflow
├── architecture_plan.md     # Cloud services, data flow, security, costs, diagram
├── reflection.md            # Project reflection and alternative designs
├── readme.md                # Top-level project summary
│
└── prototype/               # Extra-credit Flask prototype
    ├── app.py
    ├── requirements.txt
    └── README.md
```

---

## 🩺 Project Overview

Sepsis is a time-critical condition, and early identification can significantly improve outcomes.  
Hospitals often rely on fragmented vitals/labs data and rule-based alerts that fire too late.  

The goal of this project is to design a **lightweight, cloud-based pipeline** capable of:
- ingesting synthetic vitals/labs,
- processing and transforming the data,
- generating simple sepsis risk scores,
- and presenting them via a minimal web interface.

This is not a production tool — it's a conceptual, educational design showing how cloud tools can support clinical decision-making workflows.

---

## ☁️ Cloud Architecture Summary

The high-level system uses several Google Cloud Platform services:

- **Cloud Storage** – raw data landing zone  
- **Cloud Function / Cloud Run Job** – ETL + feature preparation  
- **BigQuery** – storage for engineered features + predictions  
- **Cloud SQL (optional)** – for fast dashboard lookups  
- **Cloud Run (Flask)** – small prototype dashboard/API  

A full Mermaid diagram is available in:  
📄 `architecture_plan.md` → *Section 5: Architecture Diagram*

---

## 🧪 Prototype (Extra Credit)

A small Flask application is included to illustrate how a web service could connect to cloud resources.

### Features
- Landing page (`/`)
- Cloud Storage integration demo (`/files`)
  - If no bucket is configured, the route returns a clear fallback message.

### Running the prototype
```bash
cd prototype
python -m venv venv
source venv/bin/activate   # Mac / Linux
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then visit:
- `http://127.0.0.1:5000`
- `http://127.0.0.1:5000/files`

Details are in `prototype/README.md`.

---

## 🔐 Security Considerations (High-Level)

Although the project uses synthetic data, the architecture reflects real practices:

- Minimal IAM permissions per service
- Service accounts instead of hardcoded credentials
- Environment variables or Secret Manager for secrets
- No PHI stored locally or committed to the repository

More details in `architecture_plan.md`.

---

## 💲 Cost & Operational Notes

The design intentionally avoids expensive, always-on components:

- Serverless compute scales to zero
- Minimal BigQuery usage
- Cloud SQL included only as an optional optimization
- No VMs required

---

## 📝 Reflection

A discussion of what worked, what felt uncertain, and alternative architectures considered is available in:  
📄 `reflection.md`

---

## ✔ Skills Demonstrated

- Cloud architecture design (GCP)
- Serverless compute (Cloud Functions / Cloud Run Jobs)
- ETL + feature engineering patterns
- Simple ML scoring workflow
- Flask API development
- Git & GitHub project structuring
- Technical documentation

---

## 📬 Contact

If you'd like to discuss this project or cloud-based clinical analytics, feel free to reach out.

**Email:** [jonathan.jafari@stonybrook.edu](mailto:jonathan.jafari@stonybrook.edu)
