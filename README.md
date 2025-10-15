# LLM Automated Code Reviewer

## Project Overview
**LLM Automated Code Reviewer** is a proof-of-concept backend API and dashboard designed to **automate code reviews** using the **Google Gemini LLM**.  
The system analyzes uploaded source code files (`.py`, `.js`, etc.) for **structure, readability, modularity, and adherence to best practices**, generating a detailed and structured review report.

The backend is built with **Python (Flask)**, and the LLM analysis is powered by the **Gemini API**, ensuring high-quality, actionable review reports.

---

## Features
- **📂 File Intake:** A Flask API endpoint (`/api/review`) handles code file uploads.
- **🧠 LLM Integration:** Uses the `gemini-2.5-flash-preview-05-20` model for deep, structured code analysis.
- **📊 Structured Output:** JSON schema for standardized review metrics — *Readability* and *Modularity* scores (0–100), key suggestions, and potential bugs.
- **💾 In-Memory Storage:** Reports stored temporarily in memory (can be upgraded to Firestore or PostgreSQL).
- **💻 Interactive Dashboard:** Simple HTML/JavaScript frontend to upload files and view reports.

---

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML + Vanilla JS
- **LLM:** Google Gemini API (`gemini-2.5-flash-preview-05-20`)
- **Storage:** In-memory (extendable to database)

---

## Project Setup

### Prerequisites
- **Python 3.8+**
- **Gemini API Key** — Obtain one from [Google AI Studio](https://aistudio.google.com/).

### Install Dependencies
```bash
pip install Flask requests
---

<details> <summary> Click to view Project Structure</summary>
/llm-code-reviewer
├── server.py               # Flask backend handling file upload & LLM review
├── requirements.txt        # Dependencies (optional)
├── README.md               # Project documentation
└── templates/
    └── index.html          # Dashboard UI for uploading code files

</details>
## API Endpoints
| **Endpoint**              | **Method** | **Description**                         | **Body**                       | **Response**                            |
|----------------------------|------------|------------------------------------------|--------------------------------|------------------------------------------|
| `/`                        | GET        | Serves the HTML dashboard                | None                           | HTML page                               |
| `/api/review`              | POST       | Submits a code file for review by Gemini | `multipart/form-data` (file)   | JSON `{ report_id, message }`           |
| `/api/report/<report_id>`  | GET        | Retrieves a structured JSON review report| None                           | JSON (full structured report)           |