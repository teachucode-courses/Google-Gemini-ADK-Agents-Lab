# Gemini ADK Second Agent

A simple conversational agent built with Google's Agent Development Kit (ADK). The agent is defined in `second_agent/agent.py` and uses the `gemini-3.5-flash` model through Vertex AI.

## Prerequisites

- Python installed and available in your terminal (`python3` on macOS; `py` or `python` on Windows)
- A Google Cloud project with billing enabled and the Vertex AI API enabled
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install), authenticated with an account that can use Vertex AI in the project

## Set up Vertex AI access

Authenticate with Application Default Credentials and enable the Vertex AI API for your project:

```bash
gcloud auth application-default login
gcloud services enable aiplatform.googleapis.com --project=YOUR_GOOGLE_CLOUD_PROJECT
```

Replace `YOUR_GOOGLE_CLOUD_PROJECT` with your Google Cloud project ID. Your account needs permission to use Vertex AI in that project.

## Install dependencies and configure the agent

### macOS

Run these commands from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT="YOUR_GOOGLE_CLOUD_PROJECT"
export GOOGLE_CLOUD_LOCATION="global"
```

Replace `YOUR_GOOGLE_CLOUD_PROJECT` with your project ID. These environment variables are available only in the current terminal session. Choose a location where the configured Gemini model is available.

### Windows PowerShell

Run these commands from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:GOOGLE_GENAI_USE_VERTEXAI = "TRUE"
$env:GOOGLE_CLOUD_PROJECT = "YOUR_GOOGLE_CLOUD_PROJECT"
$env:GOOGLE_CLOUD_LOCATION = "global"
```

Replace `YOUR_GOOGLE_CLOUD_PROJECT` with your project ID. These environment variables are available only in the current PowerShell session. Choose a location where the configured Gemini model is available.

If PowerShell blocks virtual-environment activation because script execution is disabled, allow locally created scripts for your user, then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

## Run the agent

Keep the virtual environment activated, Vertex AI environment variables set, and ADC credentials configured. From the project directory, start an interactive terminal session:

```shell
adk run second_agent
```

Or start the ADK web interface:

```shell
adk web .
```

Open the local URL printed by the command in your browser. Press `Ctrl+C` in the terminal to stop either command.

## Deactivate the virtual environment

When you are finished, run this in either shell:

```shell
deactivate
```
