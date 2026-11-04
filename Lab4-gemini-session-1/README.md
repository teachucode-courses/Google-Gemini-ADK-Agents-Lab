# Lab 4 - Using OpenAI GPT-4 with ADK

Run an ADK agent backed by OpenAI's GPT-4 via LiteLLM.

## Setup

```bash
python -m venv .venv
# Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
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
# Note
Agent accepts model as a string. ADK sees "openai/gpt-4" and uses its model registry to resolve the openai/ provider to its LiteLlm adapter. That adapter then calls LiteLLM, which routes the request to OpenAI. So the code doesn’t explicitly import or instantiate LiteLlm, but installing litellm lets ADK load and use it behind the scenes.