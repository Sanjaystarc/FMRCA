# main.py

import os
from google_adk.session import InMemorySessionService
from src.tools.custom_tools import fetch_historical_price_data
from src.agents.news_analyst_agent import NewsAnalystAgent
from src.agents.compliance_rag_agent import ComplianceRAGAgent
from src.agents.risk_scoring_agent import RiskScoringAgent
from src.agents.report_writer_agent import ReportWriterAgent

def run_fmrca_audit(ticker: str):
    """
    Orchestrates the sequential multi-agent workflow for the FMRCA audit.
    """
    # 1. API Key Check (Critical Step)
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY environment variable not found.")
        print("Please set it as a GitHub Codespaces Secret.")
        return

    # 2. Setup Session and Initial Data
    session = InMemorySessionService()
    
    # Fetch mock historical data (input for Risk Scoring Agent)
    price_data = fetch_historical_price_data(ticker)
    
    print(f"\n{'='*60}")
    print(f"       FMRCA AUDIT STARTING FOR {ticker}")
    print(f"{'='*60}")
    
    # 3. Instantiate Agents
    news_agent = NewsAnalystAgent()
    compliance_agent = ComplianceRAGAgent()
    risk_agent = RiskScoringAgent()
    report_agent = ReportWriterAgent()
    
    # --- 4. Sequential Execution ---

    # STEP 1: News Analysis
    print("\n[STEP 1/4] Running News Analyst (Google Search Tool)...")
    user_query = f"Analyze real-time market news and sentiment for {ticker}."
    news_output = news_agent.run(session, user_query)
    
    # Ensure the news agent provides structured output (ADK output data access)
    news_summary = news_output.output_data.get('summary', 'No detailed news summary available.')
    print(f"   -> News Summary: {news_summary[:80]}...")
    
    # STEP 2: Compliance Check (Input: News Summary)
    print("\n[STEP 2/4] Running Compliance RAG Agent (Custom Tool)...")
    compliance_output = compliance_agent.run(session, f"Analyze this news summary for compliance risk: {news_summary}")
    
    compliance_citations = compliance_output.output_data.get('citations', 'No citations found.')
    print(f"   -> RAG Citations Retrieved: {compliance_citations[:80]}...")
    
    # STEP 3: Risk Scoring (Input: Price Data & News Context for Code Execution)
    print("\n[STEP 3/4] Running Risk Scoring Agent (Code Execution Tool)...")
    risk_input = (
        f"Historical Price Data (30 days): {price_data}. "
        f"News Context: {news_summary}. "
        "Write and execute Python code using the CodeExecutionTool to calculate the 30-day Historical Volatility and state the final result."
    )
    risk_output = risk_agent.run(session, risk_input)
    
    risk_score = risk_output.output_data.get('risk_score', 'Calculation failed or not explicitly stated.')
    print(f"   -> Final Risk Score: {risk_score[:80]}...")
    
    # STEP 4: Final Report Generation
    print("\n[STEP 4/4] Generating Final Report...")
    final_input = (
        f"Compile all findings into a professional report:\n\n"
        f"NEWS: {news_summary}\n\n"
        f"COMPLIANCE CITATIONS: {compliance_citations}\n\n"
        f"RISK SCORE: {risk_score}"
    )
    final_report = report_agent.run(session, final_input)
    
    # 5. Output Final Report
    print("\n\n" + "="*60)
    print("        COMPLETED FINAL FMRCA REPORT")
    print("="*60)
    print(final_report.output_data.get('report', final_report.output_data))


if __name__ == "__main__":
    # The default ticker to analyze when the script is run
    run_fmrca_audit("GOOG")