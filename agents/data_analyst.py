from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_quant_analyst(ticker: str, raw_market_data: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite Wall Street Quantitative Analyst. 
        Your job is to interpret raw market data and technical indicators and provide a concise, structured analysis.
        Focus strictly on price action, moving averages (SMA), momentum (RSI), and volatility.
        Do not invent data; rely purely on the provided context.
        Output your analysis in professional financial terms, identifying bullish or bearish trends."""),
        ("user", "Analyze the following technical data for {ticker}:\n\n{raw_market_data}\n\nProvide a structured quantitative summary.")
    ])
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "ticker": ticker,
        "raw_market_data": raw_market_data
    })
    
    return response
