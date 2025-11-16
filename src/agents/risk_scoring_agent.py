# src/agents/risk_scoring_agent.py

from google.adk.agents import Agent # Corrected Class Name
from google.adk.tools import code_execution# Fixed Import Path

class RiskScoringAgent(Agent):
    """
    Agent responsible for quantitative risk calculation using the Code Execution Tool.
    It calculates metrics like historical volatility based on provided price data.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="RiskScoringAgent",
            model="gemini-2.5-flash",
            instruction=(
                "You are a Quantitative Risk Analyst. You will receive historical price data and market context. "
                "Your primary task is to **WRITE AND EXECUTE PYTHON CODE** using the Code Execution Tool "
                "to calculate the 30-day Historical Volatility from the provided price data list. "
                "You must use the 'pandas' and 'numpy' libraries for this calculation. "
                "The final output MUST be a JSON object with a key 'risk_score' containing the calculated volatility percentage and a brief explanation."
            ),
            # Initialize the tool class when passing it to the agent
            tools=[code_execution()],
            **kwargs
        )