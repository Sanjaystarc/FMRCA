# main.py

import os
import json
from google.adk.agents import Agent # Confirmed Agent Class Name
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

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
    
    # 2. Setup Session Service and Runner
    APP_NAME = "agents"
    USER_ID = "fmrca_user"
    SESSION_ID = f"audit_{ticker}"

    session_service = InMemorySessionService()
    session = session_service.create_session_sync(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
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
    
    # We define a single sequential process here by running agents one after the other 
    # and passing their output as input to the next agent's run_query.
    
    # --- 4. Sequential Execution ---
    
    # STEP 1: News Analysis
    runner_news = Runner(agent=news_agent, app_name=APP_NAME, session_service=session_service)
    
    print("\n[STEP 1/4] Running News Analyst (Google Search Tool)...")
    user_query = f"Analyze market news and sentiment for {ticker}."
    
    # ADK uses Event streaming; we process the events to get the final response.
    news_summary = ""
    for event in runner_news.run(user_id=USER_ID, session_id=SESSION_ID, new_message=types.Content(role='user', parts=[types.Part(text=user_query)])):
        if event.content and event.is_final_response():
            # Assume the agent returns a JSON string, which we load
            try:
                response_text = event.content.parts[0].text if event.content.parts else ""
                if response_text.strip():
                    news_output_data = json.loads(response_text)
                    news_summary = news_output_data.get('summary', response_text[:200])
                else:
                    news_summary = "No detailed news summary available."
            except json.JSONDecodeError:
                # If response is not JSON, use it as is
                news_summary = event.content.parts[0].text if event.content.parts else "No detailed news summary available."
            break
            
    print(f"   -> News Summary: {news_summary[:80]}...")
    
    # STEP 2: Compliance Check (Input: News Summary)
    runner_compliance = Runner(agent=compliance_agent, app_name=APP_NAME, session_service=session_service)
    
    print("\n[STEP 2/4] Running Compliance RAG Agent (Custom Tool)...")
    compliance_input = news_summary
    compliance_citations = ""
    for event in runner_compliance.run(user_id=USER_ID, session_id=SESSION_ID, new_message=types.Content(role='user', parts=[types.Part(text=f"Analyze this news summary for compliance risk: {compliance_input}")])):
        if event.content and event.is_final_response():
            try:
                response_text = event.content.parts[0].text if event.content.parts else ""
                if response_text.strip():
                    compliance_output_data = json.loads(response_text)
                    compliance_citations = compliance_output_data.get('citations', response_text[:200])
                else:
                    compliance_citations = "No citations found."
            except json.JSONDecodeError:
                # If response is not JSON, use it as is
                compliance_citations = event.content.parts[0].text if event.content.parts else "No citations found."
            break
            
    print(f"   -> RAG Citations Retrieved: {compliance_citations[:80]}...")
    
    # STEP 3: Risk Scoring (Input: Price Data & News Context for Code Execution)
    runner_risk = Runner(agent=risk_agent, app_name=APP_NAME, session_service=session_service)
    
    print("\n[STEP 3/4] Running Risk Scoring Agent (Code Execution Tool)...")
    risk_input = (
        f"Historical Price Data (30 days): {price_data}. "
        f"News Context: {news_summary}. "
        "Write and execute Python code using the Code Execution Tool to calculate the 30-day Historical Volatility and state the final result."
    )
    risk_score = ""
    for event in runner_risk.run(user_id=USER_ID, session_id=SESSION_ID, new_message=types.Content(role='user', parts=[types.Part(text=risk_input)])):
        if event.content and event.is_final_response():
            try:
                response_text = event.content.parts[0].text if event.content.parts else ""
                if response_text.strip():
                    risk_output_data = json.loads(response_text)
                    risk_score = risk_output_data.get('risk_score', response_text[:200])
                else:
                    risk_score = "Calculation failed or not explicitly stated."
            except json.JSONDecodeError:
                # If response is not JSON, use it as is
                risk_score = event.content.parts[0].text if event.content.parts else "Calculation failed or not explicitly stated."
            break
            
    print(f"   -> Final Risk Score: {risk_score[:80]}...")
    
    # STEP 4: Final Report Generation
    runner_report = Runner(agent=report_agent, app_name=APP_NAME, session_service=session_service)
    
    print("\n[STEP 4/4] Generating Final Report...")
    final_input = (
        f"Compile all findings into a professional report:\n\n"
        f"NEWS: {news_summary}\n\n"
        f"COMPLIANCE CITATIONS: {compliance_citations}\n\n"
        f"RISK SCORE: {risk_score}"
    )
    final_report_text = ""
    for event in runner_report.run(user_id=USER_ID, session_id=SESSION_ID, new_message=types.Content(role='user', parts=[types.Part(text=final_input)])):
        if event.content and event.is_final_response():
            try:
                response_text = event.content.parts[0].text if event.content.parts else ""
                if response_text.strip():
                    final_report_data = json.loads(response_text)
                    final_report_text = final_report_data.get('report', response_text)
                else:
                    final_report_text = "No report generated."
            except json.JSONDecodeError:
                # If response is not JSON, use it as is
                final_report_text = event.content.parts[0].text if event.content.parts else "No report generated."
            break
            
    # 5. Output Final Report
    print("\n\n" + "="*60)
    print("        COMPLETED FINAL FMRCA REPORT")
    print("="*60)
    print(final_report_text)


if __name__ == "__main__":
    run_fmrca_audit("GOOG")