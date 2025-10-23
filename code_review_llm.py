from typing import Dict, Any, Optional
import time
import os
import requests
import json
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
API_KEY = os.environ.get("GEMINI_API_KEY", "")

def review_code_with_llm(code_content: str, filename: str) -> Dict[str, Any]:
    """
    Calls the Gemini API to review the provided code content with a structured request.
    Implements retry logic with exponential backoff.
    """
    system_prompt = (
        "You are an expert Senior Software Engineer AI. Your task is to perform a meticulous "
        "code review on the provided source code. Analyze the structure, readability, "
        "modularity, and adherence to best practices. Assign scores (0-100) and provide "
        "actionable, high-quality improvement suggestions. Ensure the output is a valid JSON object "
        "that strictly adheres to the provided schema."
    )

    user_query = (
        f"Review the following code from file '{filename}'. "
        "Analyze it for readability, modularity, potential bugs, and general best practices. "
        "Provide a concise summary, assign scores for Readability and Modularity (0-100), "
        "list specific potential bugs found, and provide 3-5 key improvement suggestions. "
        "The code is:\n\n---\n{code_content}\n---"
    ).format(code_content=code_content)

    # Define the structured output schema for a reliable JSON response
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "review_summary": {"type": "STRING", "description": "A one-paragraph summary of the code's quality."},
            "readability_score": {"type": "NUMBER", "description": "Score from 0 to 100 for code readability."},
            "modularity_score": {"type": "NUMBER", "description": "Score from 0 to 100 for code modularity/architecture."},
            "suggestions": {
                "type": "ARRAY",
                "description": "List of concrete improvement suggestions.",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "area": {"type": "STRING", "description": "e.g., Naming Conventions, Error Handling, Optimization."},
                        "detail": {"type": "STRING", "description": "Detailed explanation of the suggestion."},
                        "example_code": {"type": "STRING", "description": "Optional: A snippet of improved code (use Python triple backticks if included)."}
                    },
                    "required": ["area", "detail"]
                }
            },
            "potential_bugs": {
                "type": "ARRAY",
                "description": "List of specific potential bugs or vulnerabilities identified.",
                "items": {"type": "STRING"}
            },
            "best_practices_adherence": {"type": "STRING", "description": "A short comment on how well the code adheres to industry best practices."}
        },
        "required": ["review_summary", "readability_score", "modularity_score", "suggestions", "potential_bugs"]
    }

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    headers = {'Content-Type': 'application/json'}
    # If using an external API key (not in the Canvas environment), uncomment the next line
    if API_KEY:
        headers['x-api-key'] = API_KEY

    max_retries = 5
    for attempt in range(max_retries):
        try:
            # We assume the Canvas environment handles the API key if it's empty
            response = requests.post(f"{API_URL}?key={API_KEY}", json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            # Extract the generated JSON text from the response structure
            json_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}')
            
            # Parse the JSON string into a Python dictionary
            llm_report = json.loads(json_text)
            return llm_report

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429 and attempt < max_retries - 1:
                # Handle Rate Limit: Exponential backoff
                wait_time = 2 ** attempt
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"HTTP Error during LLM call: {e}")
                # For non-recoverable errors or the last attempt
                return {"error": f"LLM API failed with status code {response.status_code}: {response.text}"}
        except Exception as e:
            print(f"General error during LLM call: {e}")
            return {"error": f"An unexpected error occurred during LLM analysis: {str(e)}"}

    return {"error": "LLM API failed after multiple retries."}
