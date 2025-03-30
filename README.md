# StockSage AI - Financial News Analyzer

StockSage AI is an advanced financial analysis tool that combines the power of Agno's agent framework, Financial Modeling Prep's market data, and OpenAI's language models to provide comprehensive stock analysis and insights.

## 🚀 Features

- **Real-time Market Data Analysis**: Leverages Financial Modeling Prep API to fetch current market metrics
- **AI-Powered News Analysis**: Uses OpenAI's GPT-4 to analyze news sentiment and market trends
- **Technical Indicators**: Calculates key technical indicators like RSI and SMA
- **Beautiful Visualization**: Clean, responsive UI for displaying analysis results
- **Comprehensive Reports**: Generates detailed analysis reports with actionable insights

## 🛠️ Technology Stack

### Core Components
1. **Agno Framework**
   - Provides the agent architecture for autonomous analysis
   - Handles task orchestration and execution flow
   - Manages state and context during analysis

2. **Financial Modeling Prep API**
   - Real-time stock price data
   - Company financial metrics
   - Market indicators and ratios
   - Historical data for technical analysis

3. **OpenAI GPT-4**
   - News sentiment analysis
   - Market trend interpretation
   - Natural language report generation
   - Context-aware recommendations

## 📊 Analysis Components

1. **Market Data Analysis**
   - Current price and changes
   - Trading volume
   - Market capitalization
   - P/E ratio and other key metrics

2. **Technical Analysis**
   - 50-day Simple Moving Average (SMA)
   - Relative Strength Index (RSI)
   - Support and resistance levels
   - Trend indicators

3. **News Sentiment Analysis**
   - Real-time news aggregation
   - Sentiment scoring
   - Impact assessment
   - Trend correlation

## 🔄 How It Works

1. **Data Collection**
   ```python
   # Agno agent fetches market data
   async def fetch_market_data(self):
       return await self.fmp_client.get_quote(symbol)
   ```

2. **Analysis Pipeline**
   ```python
   # OpenAI processes market context
   async def analyze_market_context(self):
       response = await self.openai.analyze(
           market_data=self.data,
           news_items=self.news
       )
   ```

3. **Report Generation**
   ```python
   # Agno combines all analyses
   async def generate_report(self):
       return await self.agent.execute(
           market_analysis=self.market_data,
           technical_indicators=self.indicators,
           sentiment_analysis=self.sentiment
       )
   ```

## 🌟 Key Differentiators

1. **Agno Integration**
   - Autonomous agent-based architecture
   - Structured task execution
   - Context-aware processing
   - Error handling and recovery

2. **Financial Modeling Prep**
   - Enterprise-grade financial data
   - Real-time market updates
   - Comprehensive company metrics
   - Historical data access

3. **OpenAI Capabilities**
   - Advanced language understanding
   - Context-aware analysis
   - Natural language generation
   - Pattern recognition

## 📈 Output Format

The analysis results are presented in two formats:
1. **JSON Data**: Structured data for programmatic use
2. **HTML Report**: Beautiful, responsive visualization of analysis

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stocksage-ai.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   OPENAI_API_KEY=your_key
   FMP_API_KEY=your_key
   ```

4. Run analysis:
   ```bash
   python -m src.main SYMBOL -o output_dir
   ```

## 📊 Example Output

```json
{
    "market_data": {
        "price": 933.85,
        "change": -42.87,
        "volume": 4422717,
        "market_cap": "399.46B"
    },
    "technical_indicators": {
        "sma_50": 967.40,
        "rsi": 46.10
    },
    "recommendation": "Hold",
    "risk_level": "Moderate"
}
```

## 🔒 Security

- API keys are managed securely through environment variables
- Rate limiting implemented for API calls
- Error handling for API failures

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 

Market Data (FMP API) ─┐
News Articles ─────────┼─► Agno Agent ─► OpenAI Analysis ─► Final Report
Technical Indicators ──┘ 