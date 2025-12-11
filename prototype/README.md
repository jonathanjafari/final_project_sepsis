# Sepsis Early Warning – Prototype (Flask)

This folder contains a very small Flask prototype for the HHA 504 final project.  
The goal is to demonstrate how a Python web app could integrate with a cloud resource (Google Cloud Storage).

## Files

- `app.py`  
  Simple Flask app with two routes:
  - `/` – basic landing page explaining the prototype
  - `/files` – tries to list files from a Google Cloud Storage bucket (if configured)
- `requirements.txt`  
  Python dependencies for this app.

## How to Run Locally

1. Create and activate a virtual environment (optional but recommended):
```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. (Optional) Set an environment variable for a Google Cloud Storage bucket:
```bash
   export SEPSIS_BUCKET="your-bucket-name"
```
   If you skip this step, the app will still run. The `/files` route will just show a helpful message instead of real bucket contents.

4. Run the app:
```bash
   python app.py
```

5. Open a browser and go to:
   - `http://127.0.0.1:5000/` for the home page
   - `http://127.0.0.1:5000/files` to test the Cloud Storage integration route