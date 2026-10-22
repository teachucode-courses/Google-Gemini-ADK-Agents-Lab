# Lab 3 - Using OpenAI GPT-4 with ADK

Run an ADK agent backed by OpenAI's GPT-4 via LiteLLM.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add Your OpenAI API Key

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY="your-openai-api-key"
```

## Run the Agent

```bash
python agent.py
```
