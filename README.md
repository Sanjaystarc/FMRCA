# 📊 FMRCA — Financial Market Risk & Compliance Analyst

## 🧾 Overview
- **Purpose:** The FMRCA is an autonomous Sequential Multi-Agent System that speeds up and standardizes financial risk assessment and compliance checks for a given stock ticker.
- **Problem (⚠️):** Traditional audits are slow, fragmented, and error-prone — requiring manual news review, numeric computation, and regulatory cross-checks.
- **Value Proposition (🚀):** FMRCA reduces a comprehensive audit from ~3 hours to under 10 minutes, improving decision speed by ~85% while producing auditable, verifiable outputs.

## 🏛️ Architecture
- **Type:** Sequential Multi-Agent System built on the Google Agent Development Kit (ADK).
- **Orchestration (🧭):** `main.py` orchestrates a four-stage pipeline where each agent’s JSON-structured output is passed as input to the next agent.
- **Model (🤖):** All agents are configured to use Gemini 2.5 Flash.

## 🧩 Agents & Roles
- **🔍 News Analyst Agent — Data Retrieval:** Uses the `google_search` tool to fetch real-time market news, filings and sentiment for the provided ticker. Produces a JSON object with keys like `ticker`, `summary`, and `sources`.
- **📚 Compliance RAG Agent — Knowledge Grounding:** Uses a custom tool `query_compliance_database` to retrieve relevant regulatory text (RAG). Produces a JSON object with a `citations` key listing applicable rules and context.
- **📈 Risk Scoring Agent — Quantitative Analysis:** Uses an execution tool pattern to run Python (Pandas/NumPy) to compute quantitative metrics such as 30-day historical volatility. Produces a JSON object with a `risk_score` key and explanation.
- **📝 Report Writer Agent — Synthesis & Output:** Compiles the news summary, compliance citations, and risk score into a final Markdown report (returned as a `report` key in JSON).

## ✅ Key Concepts Demonstrated
- **Multi-Agent Workflow:** Clear separation of responsibilities across specialized agents.
- **🔧 Tooling:** Demonstrates both built-in ADK tools (e.g., search) and custom tools (RAG lookup).
- **🧮 Code Execution for Analysis:** Automated code writing and execution for numeric calculations (Pandas/NumPy) inside an agent.
- **🔍 Observability:** Step-by-step logs and structured JSON outputs provide traceability for audits.

## ⚙️ Quickstart — Run Locally
1. Create and activate your Python virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set the required environment variable (you mentioned creating a GitHub secret for this):

```bash
export GOOGLE_API_KEY="your_google_api_key"
```

3. Run the main audit pipeline (default demo uses ticker `GOOG`):

```bash
python main.py
```

📝 Notes:
- If agents return plain text instead of JSON, the orchestrator will fall back to the raw text (the code includes robust JSON handling).
- The pipeline will make external requests (Google search, etc.). Ensure the `GOOGLE_API_KEY` is valid and network access is available.

## 📂 Files of Interest
- `main.py`: Orchestration and sequential runner logic.
- `src/agents/`: Agent implementations (`news_analyst_agent.py`, `compliance_rag_agent.py`, `risk_scoring_agent.py`, `report_writer_agent.py`).
- `src/tools/custom_tools.py`: Local mock tools (compliance RAG lookup, mock price fetcher).
- `requirements.txt`: Python dependencies.

## 📊 Demo Results (example run)
- Historical Volatility (demo): `18.06%` (example output produced by the Risk Scoring Agent in a sample run).
- Compliance citation example: `Rule 10b-5` referenced by the Compliance RAG Agent in the demo context.

## 🤝 Contributing
- Pull requests and issues are welcome. Please follow standard GitHub contribution workflow.

## 🧾 License
- See `LICENSE` for license details.

# FMRCA — Financial Market Risk & Compliance Analyst

## Overview
- **Purpose:** The FMRCA is an autonomous Sequential Multi-Agent System that speeds up and standardizes financial risk assessment and compliance checks for a given stock ticker.
- **Problem:** Traditional audits are slow, fragmented, and error-prone — requiring manual news review, numeric computation, and regulatory cross-checks.
- **Value Proposition:** FMRCA reduces a comprehensive audit from ~3 hours to under 10 minutes, improving decision speed by ~85% while producing auditable, verifiable outputs.

## Architecture
- **Type:** Sequential Multi-Agent System built on the Google Agent Development Kit (ADK).
- **Orchestration:** `main.py` orchestrates a four-stage pipeline where each agent’s JSON-structured output is passed as input to the next agent.
- **Model:** All agents are configured to use Gemini 2.5 Flash.

## Agents & Roles
- **News Analyst Agent — Data Retrieval:** Uses the `google_search` tool to fetch real-time market news, filings and sentiment for the provided ticker. Produces a JSON object with keys like `ticker`, `summary`, and `sources`.
- **Compliance RAG Agent — Knowledge Grounding:** Uses a custom tool `query_compliance_database` to retrieve relevant regulatory text (RAG). Produces a JSON object with a `citations` key listing applicable rules and context.
- **Risk Scoring Agent — Quantitative Analysis:** Uses an execution tool pattern to run Python (Pandas/NumPy) to compute quantitative metrics such as 30-day historical volatility. Produces a JSON object with a `risk_score` key and explanation.
- **Report Writer Agent — Synthesis & Output:** Compiles the news summary, compliance citations, and risk score into a final Markdown report (returned as a `report` key in JSON).

## Key Concepts Demonstrated
- **Multi-Agent Workflow:** Clear separation of responsibilities across specialized agents.
- **Tooling:** Demonstrates both built-in ADK tools (e.g., search) and custom tools (RAG lookup).
- **Code Execution for Analysis:** Automated code writing and execution for numeric calculations (Pandas/NumPy) inside an agent.
- **Observability:** Step-by-step logs and structured JSON outputs provide traceability for audits.

## Quickstart — Run Locally
1. Create and activate your Python virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set the required environment variable (you mentioned creating a GitHub secret for this):

```bash
export GOOGLE_API_KEY="your_google_api_key"
```

3. Run the main audit pipeline (default demo uses ticker `GOOG`):

```bash
python main.py
```

Notes:
- If agents return plain text instead of JSON, the orchestrator will fall back to use the raw text (the code includes robust JSON handling).
- The pipeline will make external requests (Google search, etc.). Ensure the `GOOGLE_API_KEY` is valid and network access is available.

## Files of Interest
- `main.py`: Orchestration and sequential runner logic.
- `src/agents/`: Agent implementations (`news_analyst_agent.py`, `compliance_rag_agent.py`, `risk_scoring_agent.py`, `report_writer_agent.py`).
- `src/tools/custom_tools.py`: Local mock tools (compliance RAG lookup, mock price fetcher).
- `requirements.txt`: Python dependencies.

## Demo Results (example run)
- Historical Volatility (demo): `18.06%` (example output produced by the Risk Scoring Agent in a sample run).
- Compliance citation example: `Rule 10b-5` referenced by the Compliance RAG Agent in the demo context.

## Contributing
- Pull requests and issues are welcome. Please follow standard GitHub contribution workflow.

## License
- See `LICENSE` for license details.
