# Agentic AI Capstone: Daily Market Intelligence Briefing

This repository contains the capstone project submission for the Learners' Space 2026 Agentic AI bootcamp.

## Problem Statement

In modern financial markets, an overwhelming volume of both structured data (price action, volume, technical indicators) and unstructured data (news, macro events, social sentiment) is generated every second. Traditional single-agent LLMs fail to effectively interpret this data because prompting a single model to act simultaneously as a rigid mathematician (Quant) and a nuanced qualitative reader (Behavioral Analyst) often leads to hallucinations or watered-down, generalized outputs.

**Solution:** A Multi-Agent System using LangGraph. This architecture assigns specialized agents to discrete tasks with customized system prompts, allowing for deep, expert-level analysis in both domains simultaneously before synthesizing the insights into a cohesive executive briefing.

## Architectural Overview

This system strictly implements the "Parallel + Aggregator" state design pattern using LangGraph. Instead of running tasks sequentially, the graph forks to execute independent analysis workflows at the same time, significantly reducing latency and ensuring strict separation of concerns.

The data flow is structured in the following sequence:

1. Initialization (START): The user provides a stock ticker (e.g., NVDA), which seeds the global LangGraph state dictionary.

2. Parallel Fan-Out (Data Gathering): The graph splits into two concurrent branches:

(a) Quantitative Branch: The fetch_data_node triggers the Market Data Tool to download recent price action and compute technical indicators (RSI, SMA, Volatility).

(b) Qualitative Branch: The fetch_news_node triggers the News Scraper Tool to pull the latest headlines and article summaries from financial RSS feeds.

3. Parallel Execution (Analysis):

(a) The raw market data is passed to the Quant Agent (analyze_quant_node), which identifies technical trends.

(b) The raw news data is passed to the Sentiment Agent (analyze_sentiment_node), which scores the market mood and identifies behavioral catalysts.

4. Synchronization Barrier (Fan-In): LangGraph natively waits for both parallel analysis branches to complete their respective supersteps before proceeding.

5. Aggregation: Both the quantitative and sentiment analyses are passed into the Aggregator Agent (aggregate_node). This principal agent synthesizes the conflicting or complementary data points into a single, cohesive executive briefing.

6. Termination (END): The completed Markdown report is saved to the file system and displayed to the user.

## Note on how to run

1. I am not sharing my personal api key. To run the files, you need to create an env file with your api key.
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```
2. To run, just enter any valid stock ticker. For example for nvidia, you can use  nvda etc.
   ```bash
   python main.py --ticker NVDA
   ```

## Example Generated Output Briefing

### Daily Market Intelligence Briefing: AAPL

#### 1. Executive Summary
Apple Inc. (AAPL) currently presents a complex investment profile characterized by strong technical momentum juxtaposed against emerging operational headwinds. From a quantitative perspective, the asset is exhibiting a robust bullish trend, trading consistently above both its 5-day and 20-day Simple Moving Averages. However, an RSI creeping toward the 70 mark suggests the stock is nearing overbought territory, warranting caution against potential short-term pullbacks.

Qualitatively, the market mood is cautiously optimistic but tempered by supply chain realities. While broad market rallies and institutional upgrades continue to provide a floor for the stock, recent reports of flagship product delays have introduced a layer of negative sentiment. The synthesis of these factors suggests that while the structural uptrend remains intact, near-term volatility is highly likely as investors digest the implications of production bottlenecks against otherwise stellar earnings expectations.

#### 2. Quantitative vs. Qualitative Matrix

| Perspective | Key Findings | Implication |
| :--- | :--- | :--- |
| **Technicals (Quant)** | Price > 20d SMA, RSI at 68.5, Volatility < 15% | Strong bullish momentum, but approaching overbought levels. |
| **Narrative (Sentiment)** | Upgrades counteracted by supply chain disruption news. | Cautious optimism; market mood score of +4. |
| **Synthesis** | Technical strength may ignore short-term macro noise. | Hold/Accumulate on dips; avoid buying market tops. |

#### 3. Key Catalysts & Risks
* **Upside Catalysts:** Impending strategic partnership announcements; broader tech-sector macroeconomic rallies.
* **Downside Risks:** Supply chain disruptions solidifying into earnings misses; RSI breaching 70 leading to rapid algorithm-driven sell-offs.

#### 4. Final Risk Assessment Score
* **Score:** 6/10
* **Justification:** While technicals are undeniably strong, the convergence of overbought momentum indicators with tangible supply chain disruptions elevates near-term behavioral and execution risk.
