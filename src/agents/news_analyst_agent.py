# src/agents/news_analyst_agent.py

from google.adk.agents import Agent # Corrected Class Name
from google.adk.tools import google_search # Fixed Import Path

class NewsAnalystAgent(Agent):
    """
    Agent responsible for searching for real-time market news and summarizing sentiment.
    It uses the built-in GoogleSearchTool.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="NewsAnalystAgent",
            model="gemini-2.5-flash",
            instruction=(
                "You are a professional Financial News Analyst. Your primary goal is to use the GoogleSearchTool "
                "to find the latest, most relevant market news, regulatory filings, and sentiment for the user's requested stock ticker. "
                "After searching, compile the results into a concise summary. The output MUST be a JSON object "
                "with the following keys: 'ticker', 'summary', and 'sources' (a list of URLs)."
            ),
            # Initialize the tool class when passing it to the agent
            tools=[(google_search)],
            **kwargs
        )