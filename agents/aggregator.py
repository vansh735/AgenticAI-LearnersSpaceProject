from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_aggregator(ticker: str, quant_analysis: str, sentiment_analysis: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Principal Investment Strategist creating a final executive briefing for a portfolio manager.
        You will receive a Quantitative Analysis and a Sentiment Analysis for a specific stock.
        Synthesize these two perspectives into a highly professional, beautifully formatted Markdown report.
        
        Your output MUST strictly follow this Markdown structure:
        # Daily Market Intelligence Briefing: [TICKER]
        
        ## 1. Executive Summary
        (A powerful 2-3 paragraph synthesis combining both the technical trends and market mood)
        
        ## 2. Quantitative vs. Qualitative Matrix
        (Create a Markdown table comparing the Technicals vs. The Narrative)
        
        ## 3. Key Catalysts & Risks
        (Bullet points of immediate concerns or upside triggers)
        
        ## 4. Final Risk Assessment Score
        (Assign a clear risk score from 1-10 (1=Safe, 10=Highly Risky) with a one-sentence justification)
        """),
        ("user", "Ticker: {ticker}\n\n=== Quantitative Analysis ===\n{quant_analysis}\n\n=== Sentiment Analysis ===\n{sentiment_analysis}\n\nGenerate the Executive Briefing.")
    ])
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "ticker": ticker,
        "quant_analysis": quant_analysis,
        "sentiment_analysis": sentiment_analysis
    })
    
    return response
