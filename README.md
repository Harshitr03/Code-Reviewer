LLM Automated Code Reviewer
Project Overview
This is a proof-of-concept backend API and dashboard designed to automate code review using the Gemini LLM. The system analyzes uploaded source code files (.py, .js, etc.) for structure, readability, modularity, and adherence to best practices, generating a detailed, structured review report.

The backend is built with Python and Flask, and the LLM analysis is powered by the Google Gemini API, utilizing structured output to ensure high-quality, actionable reports.

Features
File Intake: A robust Flask API endpoint (/api/review) handles file uploads.

LLM Integration: Utilizes the gemini-2.5-flash-preview-05-20 model for deep, structured code analysis.

Structured Output: Enforces a JSON schema for reports, providing standardized metrics like Readability and Modularity scores (0-100), key suggestions, and potential bugs.

In-Memory Storage: Reports are temporarily stored in memory (can be replaced by a database like Firestore for persistence).

Interactive Dashboard: A simple HTML/JavaScript frontend allows users to easily upload files and view the resulting review reports directly.

Project Setup
Prerequisites
Python 3.8+

A Gemini API Key: You can obtain one from Google AI Studio.

Required Python Libraries:

pip install Flask requests

Directory Structure
The Flask application expects the template file to be inside a templates directory:

/llm-code-reviewer
├── server.py
└── templates/
    └── index.html

API Key Configuration
The application is configured to read the API key from the environment variable GEMINI_API_KEY.

Local Setup (Linux/macOS):
export GEMINI_API_KEY="YOUR_API_KEY_HERE"

Local Setup (Windows PowerShell):
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"

Note: If you are using this code in a sandbox environment, the API key may be handled automatically.

Running the Application
Ensure you are in the directory containing server.py.

Run the application:
python server.py
The application will start on http://127.0.0.1:5000/.

API Endpoints
Endpoint                Method      Description                                     Request Body                            Response
/                       GET         Serves the HTML frontend dashboard.             None                                    HTML
/api/review             POST        Submits a code file for review by the LLM.      multipart/form-data with code_file      {"report_id": "...", "message": "..."}
/api/report/<report_id> GET         Retrieves the full structured JSON report.      None                                    JSON object containing review data and raw_code.

LLM Structure and Cost Control
The review_code_with_llm function uses a structured prompt and JSON schema to maximize the quality and consistency of the review. For cost control, remember:
Free Tier: If billing is not enabled, usage is hard-capped daily, preventing unexpected charges.
Quotas: If billing is enabled, you can set custom Requests per Day (RPD) limits for the Generative Language API in the Google Cloud Console.