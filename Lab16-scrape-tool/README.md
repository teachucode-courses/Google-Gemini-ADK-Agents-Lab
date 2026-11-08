# Lab 16: Build a Website-Reading Tool with Google ADK

In this lab, you will build a Google ADK agent that reads a public web page and
summarizes it. The agent uses a custom Python function instead of CrewAI's
`ScrapeWebsiteTool`.

## What the project does

The `scrape_agent` agent can:

1. Accept a web page URL from the user.
2. Check that the URL uses HTTP or HTTPS and has a hostname.
3. Check that the hostname resolves to public IP addresses.
4. Download the page and check that the response is HTML.
5. Use Beautiful Soup to remove scripts and styles and extract the page text.
6. Return up to 50,000 characters for the Gemini model to summarize.

The scraping code is in [`scrape_agent/agent.py`](scrape_agent/agent.py).
The `scrape_website` function is registered as a tool on the ADK agent.

## Prerequisites

- Python 3 installed and available in your terminal.
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Set up the project

Run these commands from the `Lab16-crewai-tool` directory.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configure your API key

Create a file named `.env` inside the `scrape_agent` directory, alongside
`agent.py`, and add your key:

```text
GOOGLE_API_KEY=your-api-key-here
```

Replace the example value with your own key. The agent calls `load_dotenv()` to
load this setting. The `.env` file is listed in `scrape_agent/.gitignore`; do
not copy your real key into source code or commit it to Git.

## Run the agent

Keep the virtual environment activated, and run these commands from the
`Lab16-crewai-tool` directory.

### Interactive terminal

```shell
adk run scrape_agent
```

### Web interface

```shell
adk web .
```

Open the local address printed in the terminal. Try asking the agent to read a
public web page and summarize it. Press `Ctrl+C` in the terminal to stop it.

When finished, deactivate the virtual environment:

```shell
deactivate
```

## How the tool handles pages

- Only `http://` and `https://` URLs are accepted.
- Pages that do not return HTML, such as PDFs or images, are rejected.
- Requests have a 15-second timeout, and redirects are not followed.
- The extracted text is limited to 50,000 characters.
- Network and scraping errors are returned to the agent so it can explain the
  problem instead of summarizing missing content.

The IP-address check is a useful introductory safeguard, not a complete
security boundary: the HTTP client resolves the hostname again when connecting.
Do not treat this sample as a hardened web-scraping service.

## Google Search vs. URL scraping

Google ADK's [Google Search tool](https://adk.dev/integrations/google-search/)
is designed for web search and grounding: the agent searches for information
and uses current web results in its response. The `scrape_website` tool has a
different job: it fetches the specific URL provided by the user and extracts
that page's text.

| User request | Google Search | `scrape_website` |
| --- | --- | --- |
| "What are the latest Gemini models?" | Ideal for finding current information | Usually unnecessary |
| "Find articles about Google ADK" | Ideal for discovering relevant pages | The user would need to provide URLs |
| "Summarize `https://example.com/article`" | May find indexed information about the page | Fetches the exact URL |
| "What does paragraph X of this URL say?" | Not designed to extract exact page text | Better fit |
| "Extract the content of this web page" | Not primarily an extraction tool | Yes |
| "Research this topic across multiple sources" | Better for discovering information across sources | Useful only when specific URLs are available |

Think of the agent as having two complementary capabilities:

```text
                  Web Reader Agent
                  /              \
        Google Search          URL Scraper
             |                      |
       discover and research     read the exact
        current information      page provided
```

### Choosing a tool

1. **The user provides a URL:** call `scrape_website(url)` to read that exact
   page.
2. **The user asks a research question:** use `google_search` to discover
   relevant, current information.
3. **The user asks for research and deeper reading:** use search to discover
   relevant pages, then scrape specific URLs if the workflow needs their full
   page content.

The tools have complementary responsibilities: search discovers information
and sources, while scraping retrieves and extracts the contents of a specified
web page.
