import os
from flask import Flask, jsonify
try:
    from google.cloud import storage
except ImportError:
    storage = None  # Allows the app to run even if the library isn't installed


app = Flask(__name__)


def list_gcs_files():
    """
    Try to list files from a Google Cloud Storage bucket.
    If no bucket is configured or something goes wrong,
    return a simple message instead.
    """
    bucket_name = os.environ.get("SEPSIS_BUCKET")

    # If no bucket is set, just return a note
    if not bucket_name:
        return ["(No bucket configured. Set SEPSIS_BUCKET env var to use GCS integration.)"]

    if storage is None:
        return ["(google-cloud-storage library not available.)"]

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs]
    except Exception as exc:
        return [f"(Error talking to GCS: {exc})"]


@app.route("/")
def index():
    """
    Simple home page that explains what this app is.
    """
    return (
        "<h1>Sepsis Early Warning Prototype</h1>"
        "<p>This is a small Flask app for the HHA 504 final project.</p>"
        "<p>Try visiting <code>/files</code> to see Cloud Storage integration.</p>"
    )


@app.route("/files")
def files():
    """
    Route that shows files from a Cloud Storage bucket (if configured),
    or a helpful message if not.
    """
    file_list = list_gcs_files()
    return jsonify({"bucket_files": file_list})


if __name__ == "__main__":
    # Run the app locally for testing
    app.run(debug=True)
