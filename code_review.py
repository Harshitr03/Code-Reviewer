import os
import uuid
import time
import requests
from flask import Flask, request, jsonify, render_template
from typing import Dict, Any, Optional
import json
from code_review_llm import review_code_with_llm

REPORT_STORE: Dict[str, Dict[str, Any]] = {}

app = Flask(__name__)

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def index():
    """Serves the simple HTML dashboard/input page."""
    return render_template('index.html')

@app.route('/api/review', methods=['POST'])
def submit_code_for_review():
    """Handles POST request to submit code for analysis."""
    # Check if a file was uploaded
    if 'code_file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    code_file = request.files['code_file']

    # Check if the filename is empty
    if code_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Ensure the file is processed and content is read
    try:
        code_content = code_file.read().decode('utf-8')
        filename = code_file.filename
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    # 1. Generate unique report ID
    report_id = str(uuid.uuid4())

    # 2. Get LLM review
    llm_report = review_code_with_llm(code_content, filename)

    if 'error' in llm_report:
        # If the LLM call failed, return the error
        return jsonify(llm_report), 500

    # 3. Store the report
    report_data = {
        "id": report_id,
        "filename": filename,
        "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "raw_code": code_content,
        "review": llm_report
    }
    REPORT_STORE[report_id] = report_data

    # 4. Return success and the report ID
    return jsonify({
        "message": "Code review initiated successfully. Report available.",
        "report_id": report_id,
        "review_summary": llm_report.get("review_summary", "Review summary not available.")
    }), 202 # 202 Accepted, processing complete (in this synchronous case)

@app.route('/api/report/<report_id>', methods=['GET'])
def get_report(report_id):
    """Handles GET request to retrieve a stored report."""
    report = REPORT_STORE.get(report_id)
    if not report:
        return jsonify({"error": f"Report with ID '{report_id}' not found."}), 404

    return jsonify(report)

# --- Run Application ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
