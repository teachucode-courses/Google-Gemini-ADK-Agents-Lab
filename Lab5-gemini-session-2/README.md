# Lab 4 - Using a Local LLM with Ollama

Run an ADK agent backed by a local Ollama model via LiteLLM.

## Prerequisites

- Ollama installed and running (https://ollama.com)

## Pull the Model

```bash
ollama pull phi
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Agent

No API key needed since the model runs locally.

```bash
python agent.py
```
