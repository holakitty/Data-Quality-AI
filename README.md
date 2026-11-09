# AI Data Quality Analyzer - Setup Guide

## Quick Start
1. Open `index.html` in your browser (or go to http://localhost:8080)
2. Configure your API key in the chatbot section
3. Upload a CSV/Excel file and start analyzing!

## Deploy the Streamlit App
1. Push this project to a GitHub repository.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**.
3. Select the repository, branch, and `app.py` as the app file.
4. Deploy. Community Cloud installs dependencies from `requirements.txt`.

Do not commit `.env`, `app_key.txt`, `.venv/`, or Streamlit secrets. Add any required credentials through the app's **Settings > Secrets** in Community Cloud.

## API Keys Required for AI Chatbot

### Option 1: GROQ
- Visit: https://console.groq.com
- Get your free API key
- Enter it in the chatbot's API Key field
- Select provider: "GROQ (Llama 3.3 70B)"

### Option 2: OpenRouter
- Visit: https://openrouter.ai/keys
- Get your API key
- Enter it in the chatbot's API Key field
- Select provider: "OpenRouter (GPT-4o-mini)"

## Project Structure
 `app.py` - Streamlit application
 `requirements.txt` - Cloud runtime dependency
 `AI_Data_Quality_Analyzer.pptx`, `Part2_Agent_Deep_Dive.pptx`, `Part3_Advanced_Topics.pptx` - Downloadable study materials

The public deployment repository contains only the app and its required presentation assets. Workspace datasets, generated reports, local credentials, and unrelated server scripts are not included.

## Starting the Servers
1. HTTP Server (serves website): `python -m http.server 8080`
2. AI Chat Server: `python ai_chat_server.py`

## API Key Setup
Create a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
```
