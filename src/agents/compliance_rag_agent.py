# src/agents/compliance_rag_agent.py

from google.adk.agents import Agent # Corrected Class Name
from src.tools.custom_tools import query_compliance_database

class ComplianceRAGAgent(Agent):
    """
    Agent responsible for checking regulatory compliance against a knowledge base.
    It uses the custom query_compliance_database tool (simulated RAG).
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="ComplianceRAGAgent",
            model="gemini-2.5-flash",
            instruction=(
                "You are a specialized Compliance Checker. Your input is a financial news summary. "
                "You MUST use the 'query_compliance_database' tool to find the most relevant regulatory rules "
                "that might be violated or applicable based on the news summary. "
                "The output MUST be a JSON object with a key 'citations' containing a list of the retrieved "
                "rule titles and the specific context provided by the tool."
            ),
            # This registers your custom function as a callable tool for the agent
            tools=[query_compliance_database],
            **kwargs
        )