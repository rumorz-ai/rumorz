
<p align="center">
    <img src="https://svgur.com/i/18SB.svg" alt="Rumorz Logo" width="150"/>
</p>

# 🚀 What is Rumorz?

Rumorz tracks 100s of sources across the web and financial markets to extract investments insights and sentiment analytics.
We index a large amount of web data in real-time and use AI Agents to 
save you time reading, staying up to date, and identifying trends and investment
opportunities.


## How does it work?

AI Agents read and analyze web data 24/7 and ingest 100s of pages of text a day into a knowledge graph, allowing
social and semantic analysis at state of the art performance.

<p align="center">
    <img src="https://github.com/user-attachments/assets/9f4c5a76-afa1-406a-bfad-d7ae07cb8c25" alt="tinyllm arc" width='500'>
</p>


## 🛠️ Install

```bash
pip install rumorz
```

## 🔒 API Access

Email othmane@rumorz.io with "Rumorz API KEY" in the subject line.

## ✅ Features
- **Screener**: a ranking of all entities in the Rumorz Graph by social metrics (mentions, sentiment, excitement, optimism, pessimism, fear, uncertainty, surprise')
- **Real-time updates**: Get real-time updates on the cryptomarket or specific entities
- **Tick-level time-series data**: get real-time amd historical sentiment data for all entities in the Graph
- **Annotated news**: Get news articles related to any entity with sentiment and AI annotations
- **Search**: search and find financial assets, companies or people in the Rumorz Graph
- **Copilot**: An Agent with knowledge of the Rumorz Python package that can generate custom scripts for you

## 📚 Use cases

- AI Agents
- Market monitoring and alerts
- Sentiment based investment and trading strategies
- Financial research, analysis and alpha generation
- Data source for AI Agents and RAG based applications
- Social media bot development: Telegram, Discord, Twitter/X etc.
- Workflow automation: emails, PDFs, reports etc.

# 🚀 Examples
    * [Ask the Copilot to generate a custom script](docs/examples/copilot.py)
    * [Various examples](docs/examples/examples.py)
    * [Plot the sentiment scores of Bitcoin over time](docs/examples/bitcoin_sentiment.py)


## FAQ

#### How do I get an API Key?
Email othmane@rumorz.io with "Rumorz API KEY" in the subject line.

#### How do I use the SDK Copilot?
The Copilot uses litellm under the hood. Just set your provider's API key as an environment variable and instantiate a RumrozCopilot with your model name. Please refer to 
the [litellm docs](https://docs.litellm.ai/docs/) for more information on 
providers/model names and authentication.

#### What are Rumorz's data sources? 
We listen to 100s of news websites and sources from the web 24/7. 

#### How does Rumorz leverage AI and Large Language Models (LLMs)?
We use LLMs for indexing data, generating summaries, and extracting various sentiment scores. We also have an anomaly
detection ML pipeline that helps us detect and filter out signal from noise to generate alerts

#### What financial assets and entities does Rumorz track? 
Rumorz tracks financial assets (crypto only for now), organizations, companies 
and people on the web. 
For now we're only tracking the crypto ecosystem but we plan to add US Stocks in the future as well.

#### How are the sentiment scores generated?
Using a combination of LLMs and NLP techniques.

#### Are AI updates using real-time data? 
Yes, any summary or update generated uses real-time data.

#### Can I use the data for detecting investments or backtesting?
Yes, the data can be used for backtesting and other analysis. Rumorz has been built with
institutional grade quality in mind. 

