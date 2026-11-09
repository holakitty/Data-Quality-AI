import os, json
from flask import Flask, request, jsonify

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

client = None
if GROQ_AVAILABLE and GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

AI_WORKPLACE_PROMPT = """You are an AI Data Quality Analyst working in an AI-powered workplace. You are an AI employee who specializes in data quality analysis. Your role is to help users identify, analyze, and resolve data quality issues in their datasets.

Dataset Context: {rows} rows, {columns} columns

User Question: {message}

Your response should:
1. Analyze the specific data quality issue
2. Provide actionable insights
3. Recommend fixes or next steps
4. Think like a data quality professional in an AI workplace

Be thorough, professional, and specific."""

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    api_provider = data.get('provider', 'groq')
    api_key = data.get('api_key', '')

    if not message:
        return jsonify({"error": "No message provided"}), 400

    key = api_key or (GROQ_API_KEY if api_provider == 'groq' else OPENROUTER_API_KEY)
    if not key:
        return jsonify({"error": f"{api_provider.upper()} API key required. Get one at groq.com or openrouter.ai"}), 401

    try:
        if api_provider == 'groq':
            if not GROQ_AVAILABLE or not client:
                return jsonify({"error": "GROQ package not installed. Run: pip install groq"}), 503
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": message}],
                max_tokens=512,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
        elif api_provider == 'openrouter':
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "AI Data Quality Analyzer"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": message}],
                    "max_tokens": 512,
                    "temperature": 0.7
                },
                timeout=30
            )
            result = resp.json()
            reply = result['choices'][0]['message']['content']
        else:
            return jsonify({"error": "Invalid provider. Use 'groq' or 'openrouter'"}), 400

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data.get('message', '')
    dataset_info = data.get('dataset_info', {})
    api_provider = data.get('provider', 'groq')
    api_key = data.get('api_key', '')

    rows = dataset_info.get('rows', 0)
    columns = dataset_info.get('columns', 0)

    prompt = AI_WORKPLACE_PROMPT.format(rows=rows, columns=columns, message=message)

    key = api_key or (GROQ_API_KEY if api_provider == 'groq' else OPENROUTER_API_KEY)
    if not key:
        return jsonify({"error": f"{api_provider.upper()} API key required"}), 401

    try:
        if api_provider == 'groq':
            if not GROQ_AVAILABLE or not client:
                return jsonify({"error": "GROQ package not installed"}), 503
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
        elif api_provider == 'openrouter':
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "AI Data Quality Analyzer"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 512,
                    "temperature": 0.7
                },
                timeout=30
            )
            result = resp.json()
            reply = result['choices'][0]['message']['content']
        else:
            return jsonify({"error": "Invalid provider"}), 400

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/keys', methods=['GET'])
def keys():
    return jsonify({
        "groq_set": bool(GROQ_API_KEY),
        "openrouter_set": bool(OPENROUTER_API_KEY),
        "groq_available": GROQ_AVAILABLE
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "service": "AI Data Quality Analyzer - Chat Server"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"AI Data Quality Analyzer - Chat Server running on port {port}")
    print(f"GROQ available: {GROQ_AVAILABLE}")
    print(f"GROQ key set: {bool(GROQ_API_KEY)}")
    print(f"OpenRouter key set: {bool(OPENROUTER_API_KEY)}")
    app.run(host='0.0.0.0', port=port, debug=False)
