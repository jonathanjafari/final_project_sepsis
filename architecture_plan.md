# Architecture & Implementation Plan – Sepsis Early Warning Pipeline

This document walks through the cloud architecture behind the sepsis early-warning use case. The goal is not to create an enterprise-grade clinical system, but to show how cloud tools can work together in a realistic, thoughtful way. The overall design leans on managed services and serverless components to keep things simple, inexpensive, and easy to maintain — which is often exactly what you want in early prototypes.

---

## 1. Service Overview and Why Each One Was Chosen

This mapping also illustrates how each piece of the design builds on earlier HHA 504 labs and the HHA 507 sepsis modeling work.

Related Module refers to the part of HHA 504 where the underlying cloud concept was introduced (e.g., serverless functions, cloud storage, managed SQL, or container deployment). It does not imply we built these exact services in that module.

| Layer     | Cloud Service                  | Purpose in the System                                                | Related Assignment / Module                         |
|-----------|--------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------|
| Storage   | Google Cloud Storage           | Landing area for raw vitals/labs CSVs.                               | Module 6 – Cloud Storage (Azure & GCP)              |
| Compute   | Cloud Function / Cloud Run Job | ETL + feature engineering from raw files into feature tables.        | Module 5 – Serverless Functions (Azure & GCP)       |
| Analytics | BigQuery                       | Stores features and predictions; supports queries and model scoring. | Module 2 – Analytics Foundations & DB Concepts      |
| Frontend  | Cloud Run (Flask)              | Simple web dashboard/API for viewing sepsis risk.                    | Module 10 – Containers & Deployment (Flask/Docker)  |
| Database  | Cloud SQL (optional)           | Fast operational lookups of current predictions for the app.         | Module 2 – Cloud Databases (Managed SQL)            |


This mix of services is intentionally serverless. Instead of running a long-lived VM, each component wakes up only when needed. That keeps costs low and avoids operational overhead.

---

## 2. How Data Moves Through the System (Narrative Explanation)

Rather than just listing steps, it’s easier to describe the flow as if you were following the data through its “day in the life” inside the cloud.

### **Data enters the system**
The pipeline begins when vitals and labs are exported from a synthetic EHR source and dropped into Cloud Storage. Think of this bucket as a simple inbox — it doesn’t do anything on its own, it just waits for new files.

### **A compute job wakes up**
Once files land in the bucket, a Cloud Function (or a scheduled Cloud Run Job) runs. This is the part that does the “real work”:  
– reading the new CSVs,  
– making sure the columns look right,  
– converting timestamps into a consistent format,  
– and building short feature windows so that each patient has a snapshot of recent vitals and labs.

If anything looks off — missing columns, badly formatted values — the job can flag it in the logs. In a real hospital, this kind of validation is extremely important.

### **Features and scores are stored where they can be queried**
After the ETL step, the engineered features are written into BigQuery. From there, a simple model can run either inside BigQuery (using BigQuery ML) or through a small Python service. The model outputs a numeric risk score and a tier like “low,” “medium,” or “high.” These predictions also end up in BigQuery.

For faster dashboard use, an optional copy of the latest predictions can be pushed into Cloud SQL. This avoids repeatedly scanning large tables when the dashboard only needs a small subset of current patients.

### **The dashboard pulls everything together**
A small Flask app running on Cloud Run serves as the clinician-facing interface. The app can fetch data directly from Cloud SQL or BigQuery. Clinicians see a list of patients with their latest sepsis risk level and a few key vitals. A detail page can show score trends over time.

This dashboard is intentionally minimal: it’s a prototype to demonstrate the integration, not a production clinical tool.

---

## 3. Security, Identity, and Governance (High-Level View)

Because this is a student project, the data is synthetic. Still, it’s worth thinking through how security *would* work if this pipeline were applied to real hospital data.

### **Identity and access control**
Each cloud component should use its own service account with only the permissions it truly needs. For example, the Flask app doesn’t need write access to Cloud Storage, and the ETL job doesn’t need permission to deploy Cloud Run. Keeping roles tightly scoped is one of the simplest ways to avoid problems.

### **Secrets and configuration**
Credentials — like database connection details — should not be hard-coded in the app. Cloud Run supports environment variables, and Google Secret Manager is the ideal place to store sensitive values. For BigQuery access, service accounts usually eliminate the need for passwords altogether.

### **Handling PHI in real environments**
If this were a real production system, several additional layers would matter: private networking, VPC connectors for Cloud Run, audit logs, and strict access review processes. But since this project only uses synthetic data, the focus stays on correct architectural patterns rather than HIPAA implementation details.

---

## 4. Cost and Operational Considerations

One advantage of the chosen architecture is that most of it scales to zero. Nothing runs unless something triggers it.

### **The main cost drivers**
- **BigQuery storage and queries.** These are usually cheap at small scale, but scanning large tables can get expensive if not planned well. Partitioning helps.
- **Cloud SQL** (if used). A managed SQL instance has a constant baseline cost because it stays online.
- **Compute jobs** (Cloud Functions / Cloud Run Jobs). These cost almost nothing unless the ETL is very heavy.

### **Why not just use a VM?**
A single VM running everything would work, but it would require patching, monitoring, and more manual setup. The whole point of this design is to show how much easier things become when serverless components handle the heavy lifting.

### **Keeping costs low**
- Store only the necessary feature tables.  
- Limit how often the model retrains.  
- Use small test datasets during development.  
- Turn off Cloud SQL if not needed for the prototype.  

In short, the architecture is intentionally lightweight and practical, but still resembles the workflow of real sepsis alerting systems used in hospitals.

## 5. Architecture Diagram (Mermaid)

Below is a simple text-based diagram that shows how the major parts of the system connect. Even if your editor doesn't render Mermaid diagrams, this is still valid for submission.

```mermaid
flowchart LR
    EHR[On-Prem / Synthetic EHR Data] -->|Exports vitals/labs CSV| CS[(Cloud Storage Bucket)]

    CS -->|New files detected / schedule| ETL[Cloud Function or Cloud Run Job<br/>(ETL + Features)]
    ETL -->|Write cleaned features| BQ[(BigQuery<br/>Feature Tables)]
    ETL -->|Optional: latest snapshots| SQL[(Cloud SQL<br/>Optional)]

    BQ -->|Model training / scoring| ML[Model Step<br/>(BigQuery ML or Python)]
    ML -->|Risk scores + tiers| BQ_P[(BigQuery<br/>Predictions Table)]
    BQ_P --> SQL

    subgraph APP[Cloud Run]
        FR[Flask App<br/>(Sepsis Dashboard)]
    end

    U[Clinician / Nurse / Informaticist] -->|Views risk list| FR
    FR -->|Reads latest predictions| SQL
    FR -->|Optional historical views| BQ
```
