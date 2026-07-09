import requests
from bs4 import BeautifulSoup
from typing import List

def get_mock_headlines(ticker: str) -> str:
    return f"""
    Recent Headlines for {ticker} (Mock Fallback Data):
    1. {ticker} reports robust quarterly earnings, beating analyst expectations. (Sentiment: Positive)
    2. Supply chain disruptions cause minor delays for {ticker}'s flagship product. (Sentiment: Negative)
    3. Industry analysts upgrade {ticker} stock to 'Buy' amidst market rally. (Sentiment: Positive)
    4. Regulatory scrutiny increases in {ticker}'s primary operating sector. (Sentiment: Negative)
    5. {ticker} announces strategic partnership to expand into emerging markets. (Sentiment: Positive)
    """

def get_recent_news(ticker: str) -> str:
    url = f"https://finance.yahoo.com/rss/headlines?s={ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, features='xml')
        items = soup.find_all('item')
        
        if not items:
            return get_mock_headlines(ticker)
            
        output = [f"Recent News Headlines for {ticker}:", "-" * 50]
        
        for i, item in enumerate(items[:5]):
            title = item.title.text if item.title else "No Title"
            pub_date = item.pubDate.text if item.pubDate else "Unknown Date"
            description = item.description.text if item.description else "No description available."
            
            output.append(f"{i+1}. [{pub_date}] {title}")
            output.append(f"   Summary: {description}\n")
            
        return "\n".join(output)
        
    except requests.exceptions.RequestException as e:
        # Fallback to mock data if the API call fails to prevent pipeline crash
        print(f"Warning: News scraping failed for {ticker} ({str(e)}). Using fallback data.")
        return get_mock_headlines(ticker)
