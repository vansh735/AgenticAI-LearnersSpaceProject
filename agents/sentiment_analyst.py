from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def run_sentiment_analyst(ticker: str, raw_news_data: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Financial Journalist and Behavioral Economist.
        Your job is to read recent news headlines and summaries about a company and evaluate the market's mood.
        Your output must include:
        1. An overall 'Market Mood Score' from -10 (Extremely Bearish) to +10 (Extremely Bullish).
        2. A concise analysis of the driving macro and micro factors behind the news.
        3. Potential short-term behavioral risks or catalysts based on the headlines.
        Use a professional, objective tone."""),
        ("user", "Analyze the following recent news for {ticker}:\n\n{raw_news_data}\n\nProvide your detailed sentiment analysis.")
    ])
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    parser = StrOutputParser()
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "ticker": ticker,
        "raw_news_data": raw_news_data
    })
    
    return response
