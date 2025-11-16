from google_adk.agents import LlmAgent

class ReportWriterAgent(LlmAgent):
    """
    Agent responsible for compiling the outputs from all preceding agents 
    (News, Compliance, Risk Scoring) into the final professional report.
    It does not use any tools.
    """
    def __init__(self, **kwargs):
        super().__init__(
            name="ReportWriterAgent",
            model="gemini-2.5-flash",
            # The instruction mandates compilation and formatting, not new analysis
            instruction=(
                "You are the final Report Generator. Your input contains three distinct sections: "
                "NEWS, COMPLIANCE CITATIONS, and RISK SCORE. "
                "You MUST compile all this information into a single, professional, "
                "well-formatted Markdown report with clear headings (e.g., '## Compliance Findings'). "
                "Do not introduce any new analysis or information; strictly synthesize the provided data. "
                "The final output MUST be a JSON object with a key 'report' containing the complete Markdown text."
            ),
            # This agent requires no tools
            tools=[],
            **kwargs
        )