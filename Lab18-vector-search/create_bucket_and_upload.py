import os
from google.cloud import storage

# 1. Configuration
PROJECT_ID = "jovial-coral-423517-h8"
LOCATION = "us-central1"
BUCKET_NAME = "tuc-vector-search-bucket-1"
BLOB_NAME = "books.txt"

# Path to books.txt in the same folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_FILE_PATH = os.path.join(CURRENT_DIR, "books.txt")

# 2. Initialize Cloud Storage Client
storage_client = storage.Client(project=PROJECT_ID)

# 3. Create Bucket (if not already existing)
bucket = storage_client.bucket(BUCKET_NAME)
if not bucket.exists():
    bucket = storage_client.create_bucket(bucket, location=LOCATION)
    print(f"Bucket '{BUCKET_NAME}' created successfully in {LOCATION}!")
else:
    print(f"Bucket '{BUCKET_NAME}' already exists.")

# 4. Upload books.txt into the bucket
blob = bucket.blob(BLOB_NAME)
blob.upload_from_filename(LOCAL_FILE_PATH)
print(f"Successfully uploaded '{LOCAL_FILE_PATH}' to 'gs://{BUCKET_NAME}/{BLOB_NAME}'!")
