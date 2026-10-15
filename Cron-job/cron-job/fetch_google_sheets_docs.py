import hashlib
import json
import os
import time
import logging

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Configure logging
logging.basicConfig(
    filename='fetch_google_sheets_docs.log',  # Log file name
    level=logging.INFO,                      # Log level (INFO, DEBUG, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)
# Google API Configuration
SERVICE_ACCOUNT_FILE = 'credentials/credentials.json'

# Google Sheets Configuration
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1C6MjJsFjdcDvyTGTb_xaO3JcpNUTelBadLwyiw1qT1A'
RANGE_NAME = 'googlesheet!A1:Z'
SHEET_HASH_FILE = 'sheet_hash.json'

# Google Docs Configuration
DOCS_SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
DOCUMENT_ID = '1wY5nZsDE56X2sCh5KlzjUyDL9rgwC__u6nyXVHcSQDU'
DOC_HASH_FILE = 'doc_last_modified.json'

def get_sheets_data():
    """Fetch data from Google Sheets."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SHEETS_SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    return values

def calculate_hash(data):
    """Generate a hash from the fetched data to track changes."""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()

def check_sheets_updates():
    """Checks for updates in Google Sheets."""
    data = get_sheets_data()
    new_hash = calculate_hash(data)

    # Load last stored hash
    if os.path.exists(SHEET_HASH_FILE):
        with open(SHEET_HASH_FILE, 'r') as f:
            last_hash = json.load(f).get("hash")
    else:
        last_hash = None

    if new_hash != last_hash:
        print("Google Sheet has been updated!")
        with open(SHEET_HASH_FILE, 'w') as f:
            json.dump({"hash": new_hash}, f)
    else:
        print("No changes detected in Google Sheet.")

def get_doc_metadata():
    """Fetch last modified time of Google Doc."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=DOCS_SCOPES)
    service = build('docs', 'v1', credentials=creds)
    
    doc = service.documents().get(documentId=DOCUMENT_ID).execute()
    return doc.get('title'), doc.get('revisionId')

def check_docs_updates():
    """Checks for updates in Google Docs."""
    title, revision_id = get_doc_metadata()

    # Load last stored revision
    if os.path.exists(DOC_HASH_FILE):
        with open(DOC_HASH_FILE, 'r') as f:
            last_revision = json.load(f).get("revisionId")
    else:
        last_revision = None

    if revision_id != last_revision:
        print(f"Google Doc '{title}' has been updated!")
        with open(DOC_HASH_FILE, 'w') as f:
            json.dump({"revisionId": revision_id}, f)
    else:
        print("No changes detected in Google Doc.")

if __name__ == "__main__":
    check_sheets_updates()
    check_docs_updates()
