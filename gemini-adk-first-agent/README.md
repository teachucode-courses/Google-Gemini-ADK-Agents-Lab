# Gemini ADK First Agent

A simple conversational agent built with Google's Agent Development Kit (ADK). The agent is defined in `first_agent/agent.py` and uses the `gemini-3.5-flash` model.

## Prerequisites

- Python installed and available in your terminal (`python3` on macOS; `py` or `python` on Windows)
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## macOS

Run these commands from the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

Replace `YOUR_GOOGLE_API_KEY` with your key. The environment variable is available only in the current terminal session.

## Windows PowerShell

Run these commands from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
```

Replace `YOUR_GOOGLE_API_KEY` with your key. The environment variable is available only in the current PowerShell session.

If PowerShell blocks virtual-environment activation because script execution is disabled, allow locally created scripts for your user, then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

## Run the agent

Keep the virtual environment activated and the API key set. From the project directory, start an interactive terminal session:

```shell
adk run first_agent
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
