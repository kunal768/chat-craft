
# 🕒 Cron-Job: Google Sheets & Docs Change Monitor

This project monitors changes in **Google Sheets** and **Google Docs** using a Python script triggered by a Go-based cron scheduler every 5 minutes. If any changes are detected in the specified range or document, they are logged locally.

> Ideal for automation, internal dashboards, and passive document monitoring.

---

## 🔧 What It Does

- ⏰ A Go cron scheduler (`robfig/cron/v3`) runs every 5 minutes.
- 🐍 It triggers `fetch_google_sheets_docs.py`, a Python script that:
  - Reads data from a Google Sheet (via Google Sheets API)
  - Checks revision ID of a Google Doc (via Google Docs API)
- 🧠 Compares data with the last known state stored in:
  - `sheet_hash.json` (for Sheets)
  - `doc_last_modified.json` (for Docs)
- 📋 Logs messages when updates are detected.

---

## 🧰 Tech Stack

| Tech        | Usage                                  |
|-------------|----------------------------------------|
| Python      | Google API integration logic           |
| Go          | Cron scheduler                         |
| JSON        | For tracking previous state            |
| Google APIs | Sheets & Docs integration              |

---

## 📁 Project Structure

```
cron-job-service/
├── cron_job/
│   ├── cron_job.go                  # Go cron scheduler
│   ├── fetch_google_sheets_docs.py # Python logic
│   ├── requirements.txt            # Python dependencies
│   ├── doc_last_modified.json      # Stores last Google Doc revision ID
│   ├── sheet_hash.json             # Stores Google Sheet hash
│   ├── fetch_google_sheets_docs.log # Optional log file
│   └── credentials/
│       └── credentials.json        # Google service account key (ignored by Git)
├── README.md
├── .gitignore
└── commands.txt
```

---

## 🛠 Prerequisites

- Python 3.x
- Go 1.16 or later
- Git
- Google Cloud project with:
  - Sheets API and Docs API enabled
  - A service account key in JSON format

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Chat-craft/Cron-job.git
cd Cron-job
```

---

### 2. Set up Python

```bash
cd cron_job
python -m venv venv
venv\Scripts\activate   # (Windows)
# OR
source venv/bin/activate   # On Linux/Mac

pip install -r requirements.txt
```

✅ (Optional) Test the Python script:
```bash
python fetch_google_sheets_docs.py
```

---

### 3. Set up Go Environment

If needed, set your GOPATH to a user-friendly location (especially on Windows):

```powershell
$env:GOPATH="C:\Users\Checkout\go"
```

Install cron dependency and run the Go scheduler:

```bash
go get github.com/robfig/cron/v3
go run cron_job.go
```

---

### 🔐 Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable:
   - Google Sheets API
   - Google Docs API
4. Generate a service account and download the `credentials.json`
5. Save the file as:
   ```
   cron_job/credentials/credentials.json
   ```

---

## 🧪 Tests

Basic unit tests are available in:

```
cron_job/tests/test_fetch_google_sheets_docs.py
```

Run them with:

```bash
python -m unittest cron_job.tests.test_fetch_google_sheets_docs
```

---
