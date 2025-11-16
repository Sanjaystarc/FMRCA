from google_adk.agents import LlmAgent
from google_adk.tools.google_search import GoogleSearchTool

class NewsAnalystAgent(LlmAgent):
    """
    Agent responsible for searching for real-time market news and summarizing sentiment.
    It uses the built-in GoogleSearchTool.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="NewsAnalystAgent",
            model="gemini-2.5-flash",
            # The instruction guides the agent on when and how to use the tool
            instruction=(
                "You are a professional Financial News Analyst. Your primary goal is to use the GoogleSearchTool "
                "to find the latest, most relevant market news, regulatory filings, and sentiment for the user's requested stock ticker. "
                "After searching, compile the results into a concise summary. The output MUST be a JSON object "
                "with the following keys: 'ticker', 'summary', and 'sources' (a list of URLs)."
            ),
            # This is the tool available to the agent
            tools=[GoogleSearchTool()],
            **kwargs
        )