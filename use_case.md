# Use Case: Cloud-Based Sepsis Early Warning & Monitoring Pipeline

## 1. Problem Statement

Sepsis continues to be one of the most challenging conditions for hospitals because it can progress quickly and often presents with subtle early signs. In many settings, clinicians rely on simple rule-based alerts inside the EHR—usually SIRS criteria or basic thresholds—which often fire too late or create alert fatigue. Nurses and physicians may miss the early physiologic changes that signal deterioration, simply because relevant vitals and labs are scattered across different screens and updated at different times.

The idea behind this project is to better organize those signals and give clinical teams a clearer, more timely view of which patients may be heading toward sepsis. The goal is not to create a full production tool but to outline how a cloud-based pipeline could ingest data, run a lightweight model, and surface straightforward risk information.

**Intended users include:**

- ED and inpatient clinicians who want quick insight into patients at risk  
- Charge nurses or rapid-response teams monitoring multiple units  
- Clinical informatics and quality teams interested in sepsis detection performance  

The solution uses *synthetic or de-identified data* only. This allows the design to mimic a realistic workflow without touching real PHI.

---

## 2. Data Sources

For this project, the data is meant to mirror what a hospital typically collects during an inpatient encounter, but in a simplified format:

### **Vitals**
Common time-series measurements such as:
- heart rate  
- respiratory rate  
- temperature  
- oxygen saturation  
- systolic/diastolic blood pressure and MAP  

Each row includes a timestamp, patient identifier, and encounter ID.

### **Labs**
Key lab values associated with sepsis severity, for example:
- lactate  
- white blood cell count  
- creatinine  
- platelets  
- bilirubin  

Each lab result includes a collection time, patient ID, and encounter ID.

### **Encounter metadata**
Basic admission information such as:
- admit time  
- location or unit (ED, floor, ICU)  
- discharge time  
- a synthetic label indicating whether the patient met sepsis criteria during the encounter (used only for training/evaluation)

All files are produced as CSVs to keep things simple and are delivered to a Cloud Storage bucket.

---

## 3. Basic Workflow (High-Level)

The pipeline is intentionally straightforward and follows a step-by-step pattern similar to what many hospitals already do for analytics work, but adapted for cloud services:

### **1. Data export to Cloud Storage**
Synthetic vitals, labs, and encounter files are periodically written to a Google Cloud Storage bucket. These files act as the “raw landing zone.”

### **2. ETL and feature preparation**
A scheduled Cloud Function (or Cloud Run Job) picks up new files, checks that the expected columns exist, and cleans or converts fields where needed. It also creates short rolling windows of vitals and pulls in the most recent lab values for each active patient.  
The processed features are then written to **BigQuery**.

### **3. Generating sepsis risk scores**
A simple sepsis-risk model—either a BigQuery ML model or a small Python model—runs on the newly created features. It produces a score between 0 and 1, along with a basic tier (low, medium, high) to make it easier to interpret.  
Outputs are stored in a BigQuery table, with an optional copy in Cloud SQL for faster dashboard queries.

### **4. Displaying risk to end users**
A Flask app deployed on Cloud Run gives clinicians a lightweight dashboard. It shows:
- a current list of inpatients with their latest risk tier  
- the unit they are on  
- a few recent vitals or labs  
- an optional patient-detail view showing how the score has changed over time  

This is not meant to be a polished clinical UI—just a simple prototype to demonstrate how cloud components can work together.

### **5. Logging and monitoring**
Cloud Logging tracks errors, failed ETL steps, and model execution time. This mirrors how data teams would keep an eye on a real clinical decision support pipeline.

---

## Summary

This use case walks through a realistic—but still manageable—scenario: using cloud resources to collect vital signs and labs, clean and organize them, run a basic predictive model, and give clinicians a simple way to review sepsis risk. The emphasis is on the workflow and architecture rather than building a production-grade sepsis alerting tool.
