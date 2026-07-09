from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from tools.market_data import get_market_data
from tools.news_scraper import get_recent_news
from agents.data_analyst import run_quant_analyst
from agents.sentiment_analyst import run_sentiment_analyst
from agents.aggregator import run_aggregator

class AgentState(TypedDict):
    ticker: str
    raw_market_data: str
    raw_news_data: str
    quant_analysis: str
    sentiment_analysis: str
    final_briefing: str

def fetch_data_node(state: AgentState) -> dict:
    print(f"-> Fetching Market Data for {state['ticker']}...")
    data = get_market_data(state['ticker'])
    return {"raw_market_data": data}

def fetch_news_node(state: AgentState) -> dict:
    print(f"-> Fetching News Data for {state['ticker']}...")
    news = get_recent_news(state['ticker'])
    return {"raw_news_data": news}

def analyze_quant_node(state: AgentState) -> dict:
    print("-> Running Quantitative Analysis...")
    analysis = run_quant_analyst(state['ticker'], state['raw_market_data'])
    return {"quant_analysis": analysis}

def analyze_sentiment_node(state: AgentState) -> dict:
    print("-> Running Sentiment Analysis...")
    analysis = run_sentiment_analyst(state['ticker'], state['raw_news_data'])
    return {"sentiment_analysis": analysis}

def aggregate_node(state: AgentState) -> dict:
    print("-> Aggregating insights into Final Briefing...")
    briefing = run_aggregator(
        state['ticker'], 
        state['quant_analysis'], 
        state['sentiment_analysis']
    )
    return {"final_briefing": briefing}

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("fetch_data", fetch_data_node)
    workflow.add_node("fetch_news", fetch_news_node)
    workflow.add_node("analyze_quant", analyze_quant_node)
    workflow.add_node("analyze_sentiment", analyze_sentiment_node)
    workflow.add_node("aggregate", aggregate_node)
    
    workflow.add_edge(START, "fetch_data")
    workflow.add_edge(START, "fetch_news")
    
    workflow.add_edge("fetch_data", "analyze_quant")
    workflow.add_edge("fetch_news", "analyze_sentiment")
    
    workflow.add_edge("analyze_quant", "aggregate")
    workflow.add_edge("analyze_sentiment", "aggregate")
    
    workflow.add_edge("aggregate", END)
    
    # Compile the graph into a runnable application
    app = workflow.compile()
    return app
