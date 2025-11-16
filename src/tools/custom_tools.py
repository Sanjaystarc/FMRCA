import numpy as np
from typing import List, Dict, Any

# --- MOCK KNOWLEDGE BASE ---
# These documents simulate the external knowledge base (Vector Store) 
# that the Compliance RAG Agent would query.
COMPLIANCE_DOCS = [
    {
        "id": "A-101", 
        "title": "Rule 10b-5: Anti-Fraud Provisions", 
        "text": "It is unlawful to make any untrue statement of a material fact or to omit to state a material fact... This rule is central to preventing communication of misleading information about a company's financial health or legal status.",
        "category": "Fraud"
    },
    {
        "id": "B-205", 
        "title": "Regulation FD: Fair Disclosure", 
        "text": "Whenever an issuer, or any person acting on its behalf, discloses any material nonpublic information, the issuer shall make public disclosure of that information simultaneously.",
        "category": "Disclosure"
    },
]

def query_compliance_database(news_summary_query: str) -> List[Dict]:
    """
    [CUSTOM TOOL] Searches the internal compliance knowledge base for relevant rules.

    This function simulates a complex RAG lookup against financial regulatory texts, 
    returning the most relevant documents based on the news context.

    Args:
        news_summary_query: The summarized news event that requires a compliance check.

    Returns:
        A list of up to two most relevant compliance documents (ID, Title, and Text).
    """
    # --- SIMULATED RAG LOGIC ---
    query_lower = news_summary_query.lower()
    
    # Check for fraud/misleading information keywords
    if "misleading" in query_lower or "omission" in query_lower or "untrue statement" in query_lower:
        # Returns the Anti-Fraud rule (A-101)
        return [doc for doc in COMPLIANCE_DOCS if doc['id'] == 'A-101']
    
    # Check for selective disclosure keywords
    elif "private meeting" in query_lower or "select shareholders" in query_lower or "nonpublic information" in query_lower:
        # Returns the Fair Disclosure rule (B-205)
        return [doc for doc in COMPLIANCE_DOCS if doc['id'] == 'B-205']
    
    else:
        # Default or fallback retrieval
        return [COMPLIANCE_DOCS[0]]


def fetch_historical_price_data(ticker_symbol: str) -> Dict[str, Any]:
    """
    [MOCK DATA TOOL] Fetches mock historical closing price data over 30 days.

    This function simulates an API call to a financial data provider and provides 
    the necessary raw data for the Risk Scoring Agent's code execution.

    Args:
        ticker_symbol: The stock ticker (e.g., 'GOOG').

    Returns:
        A dictionary containing the ticker and a list of 30 mock closing prices.
    """
    # Ensures the mock data is the same every time the script runs (reproducible)
    np.random.seed(42)  
    
    # Base price centered around 150, with realistic-looking daily fluctuations
    base_price = 150.0
    daily_returns = np.random.normal(0, 0.01, 30)  # Mean 0, StDev 1%
    
    # Generate cumulative prices
    prices = [base_price]
    for r in daily_returns:
        prices.append(prices[-1] * (1 + r))
    
    # Use only 30 prices and round to 2 decimal places
    closing_prices = [round(p, 2) for p in prices[1:]]

    return {
        "ticker": ticker_symbol,
        "days": 30,
        "prices": closing_prices,
        "description": "30-day simulated historical closing prices for quantitative analysis."
    }