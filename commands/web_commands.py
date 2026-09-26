import webbrowser
from urllib.parse import quote_plus


def open_website(site):
    """Open a supported website."""

    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "chatgpt": "https://chatgpt.com",
    }

    site = site.lower().strip()

    if site in sites:
        webbrowser.open(sites[site])
        return f"Opening {site}."

    return f"I don't know the website {site}."


def search_web(query):
    """Search Google for a query."""

    query = query.strip()

    if not query:
        return "What would you like me to search for?"

    url = f"https://www.google.com/search?q={quote_plus(query)}"

    webbrowser.open(url)

    return f"Searching the web for {query}."


def execute_web_command(command):
    """Handle web-related commands."""

    command = command.lower().strip()

    # Open websites
    if command.startswith("open "):
        site = command[5:].strip()

        if site in [
            "google",
            "youtube",
            "gmail",
            "github",
            "chatgpt",
        ]:
            return open_website(site)

    # Search commands
    search_phrases = [
        "search for ",
        "search ",
        "google ",
        "look up ",
    ]

    for phrase in search_phrases:
        if command.startswith(phrase):
            query = command[len(phrase):].strip()
            return search_web(query)

    return None