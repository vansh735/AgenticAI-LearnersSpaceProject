import os
import argparse
from dotenv import load_dotenv
from orchestration.graph import build_graph

def main():
    load_dotenv()
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not found. Please check your .env file.")
        return
      
    parser = argparse.ArgumentParser(description="Generate an Agentic AI Market Briefing.")
    parser.add_argument(
        "--ticker", 
        type=str, 
        default="NVDA", 
        help="Stock ticker symbol to analyze (e.g., AAPL, TSLA, NVDA)"
    )
    args = parser.parse_args()
    target_ticker = args.ticker.upper()

    print(f"\n{'='*50}")
    print(f"INITIALIZING SYSTEM FOR TICKER: {target_ticker}")
    print(f"{'='*50}\n")

    app = build_graph()

    initial_state = {
        "ticker": target_ticker,
        "raw_market_data": "",
        "raw_news_data": "",
        "quant_analysis": "",
        "sentiment_analysis": "",
        "final_briefing": ""
    }

    print("Starting multi-agent parallel execution...")
    
    final_state = app.invoke(initial_state)

    briefing = final_state.get("final_briefing", "Error: No briefing generated.")

    output_filename = f"market_briefing_{target_ticker}.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(briefing)
        print(f"\n[SUCCESS] Executive Briefing saved to '{output_filename}'.")
    except Exception as e:
        print(f"\n[ERROR] Failed to save briefing to file: {e}")

    print(f"\n{'='*50}")
    print(f" FINAL EXECUTIVE BRIEFING ")
    print(f"{'='*50}\n")
    print(briefing)
    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    main()
