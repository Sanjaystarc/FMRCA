from google_adk.agents import LlmAgent
from google_adk.tools.code_execution import CodeExecutionTool

class RiskScoringAgent(LlmAgent):
    """
    Agent responsible for quantitative risk calculation using the Code Execution Tool.
    It calculates metrics like historical volatility based on provided price data.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="RiskScoringAgent",
            model="gemini-2.5-flash",
            # The instruction mandates the use of the Code Execution Tool
            instruction=(
                "You are a highly skilled Quantitative Risk Analyst. You will receive historical price data and market context. "
                "Your primary task is to **WRITE AND EXECUTE PYTHON CODE** using the CodeExecutionTool "
                "to calculate the 30-day Historical Volatility from the provided price data list. "
                "You must use the 'pandas' and 'numpy' libraries for this calculation. "
                "The final output MUST be a JSON object with a key 'risk_score' containing the calculated volatility percentage and a brief explanation."
            ),
            # This is the tool available to the agent for code execution
            tools=[CodeExecutionTool()],
            **kwargs
        )