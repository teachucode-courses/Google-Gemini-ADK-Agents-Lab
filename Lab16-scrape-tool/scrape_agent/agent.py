"""Define the website-reading tool and the ADK agent that uses it."""

# Agent is the Google ADK class used to configure an AI agent.
from google.adk.agents import Agent

# load_dotenv reads settings from a local .env file into environment variables.
from dotenv import load_dotenv

# These standard-library modules help check whether a URL points to a public IP.
import ipaddress
import socket

# urlparse splits a URL into parts such as its scheme (https) and hostname.
from urllib.parse import urlparse

# requests downloads the page; BeautifulSoup turns its HTML into readable text.
import requests
from bs4 import BeautifulSoup


# Load local environment settings before configuring the agent.
load_dotenv()


# ---------------------------------------------------------
# Custom website scraping tool
# This function plays the role of CrewAI's ScrapeWebsiteTool in this example.
# ---------------------------------------------------------

def scrape_website(website_url: str) -> dict:
    """Download a public web page and return its readable text.

    Args:
        website_url: The complete HTTP or HTTPS address to read.

    Returns:
        A dictionary with ``status`` and either the page ``url`` and ``content``,
        or an ``error`` message if the page could not be read.
    """

    try:
        # Split the address into parts so we can check the protocol and hostname.
        parsed = urlparse(website_url)

        # Only allow web page protocols; other schemes (such as file:) are rejected.
        if parsed.scheme not in {"http", "https"}:
            return {
                "status": "error",
                "error": "Only HTTP and HTTPS URLs are supported.",
            }

        # A URL like "https://" has no hostname, so there is nowhere to connect.
        if not parsed.hostname:
            return {
                "status": "error",
                "error": "Invalid URL. A hostname is required.",
            }

        # Look up the hostname to find the IP addresses it currently points to.
        addresses = socket.getaddrinfo(parsed.hostname, None)

        # Reject the address if any DNS result is not globally routable.
        # This is a useful basic check, but requests resolves the hostname again
        # when it connects, so this check alone is not a complete security barrier.
        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                return {
                    "status": "error",
                    "error": "Private or reserved network addresses are not allowed.",
                }

        # Download the page. The timeout prevents waiting forever if the site
        # does not respond. Redirects are not followed automatically.
        response = requests.get(
            website_url,
            timeout=15,
            allow_redirects=False,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; ADKWebReader/1.0)"
                )
            },
        )

        # Turn HTTP error responses (such as 404 or 500) into an exception.
        response.raise_for_status()

        # Check the response type before treating its contents as a web page.
        content_type = response.headers.get(
            "content-type",
            ""
        ).lower()

        # For example, a PDF or image is not HTML that this tool can summarize.
        if "text/html" not in content_type:
            return {
                "status": "error",
                "error": (
                    "The URL did not return an HTML web page. "
                    f"Content-Type: {content_type}"
                ),
            }

        # Parse the HTML response so we can remove elements and extract text.
        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Scripts, styles, and noscript fallback text are usually not useful
        # when the goal is to summarize the visible page.
        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        # Join the remaining page text with spaces and trim extra whitespace.
        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        # Keep the result to at most 50,000 characters so very long pages do not
        # send an excessive amount of text to the agent.
        text = text[:50_000]

        # Use a consistent success shape: status, original URL, and page text.
        return {
            "status": "success",
            "url": website_url,
            "content": text,
        }

    # requests raises RequestException for network problems, timeouts, and
    # unsuccessful HTTP responses. Return the message so the agent can explain it.
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": f"Unable to fetch website: {str(e)}",
        }

    # Catch other unexpected problems so the tool reports an error instead of
    # returning partial page content. During development, investigate these
    # errors rather than treating this broad catch as a substitute for debugging.
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unable to scrape website: {str(e)}",
        }


# ---------------------------------------------------------
# Agent
# The ADK uses this object as the entry point for the application.
# ---------------------------------------------------------

root_agent = Agent(
    # The name identifies the agent in the ADK application.
    name="web_reader_agent",

    # Choose the Gemini model that will interpret and summarize the page text.
    model="gemini-2.5-flash",

    # A short description of the agent's purpose.
    description=(
        "An agent that can read and summarize web pages "
        "using a website scraping tool."
    ),

    # These instructions tell the model when and how to use the scraping tool.
    instruction="""
You are a web content analyst.

When the user provides a URL or asks you to read a webpage:

1. Use the scrape_website tool to retrieve the page content.
2. Read and analyze the returned content.
3. Provide a clear and concise summary.
4. If the user asks about a specific topic on the page,
   focus your analysis on that topic.
5. Always mention the source URL in your response.

If the scraping tool returns an error, explain the problem
to the user instead of attempting to summarize the page.
""",

    # Register the Python function as a tool the agent can call.
    tools=[
        scrape_website,
    ],
)