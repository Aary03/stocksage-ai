import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    FMP_API_KEY = os.getenv('FMP_API_KEY')
    
    # Model Configuration
    DEFAULT_MODEL_ID = "gpt-4-turbo-preview"
    
    # Agent Configuration
    DEFAULT_TEMPERATURE = 0.3
    MAX_TOKENS = 4000
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    
    # News Analysis Configuration
    DEFAULT_NEWS_LIMIT = 10
    SENTIMENT_THRESHOLD = 0.1
    
    # Technical Analysis Configuration
    TECHNICAL_INDICATORS = [
        'SMA-50', 'RSI'
    ]
    
    # Analysis Prompt Template
    ANALYSIS_PROMPT_TEMPLATE = """
    Please analyze {symbol} based on the following data:

    Market Data:
    - Current Price: ${price}
    - Daily Change: ${change} ({change_percent}%)
    - Volume: {volume}
    - 52-Week Range: ${low_52w} - ${high_52w}
    - Market Cap: ${market_cap}
    - P/E Ratio: {pe_ratio}

    Technical Indicators:
    - 50-day SMA: ${sma_50}
    - RSI (14-day): {rsi}

    Recent News:
    {news_summary}

    Please provide a comprehensive analysis including:
    1. Market Overview
       - Current price action and market position
       - Volume analysis and market cap significance
       - Valuation metrics assessment

    2. Technical Analysis
       - Price relative to 50-day SMA (trend direction)
       - RSI interpretation (overbought/oversold conditions)
       - Overall technical outlook

    3. News Sentiment Analysis
       - Key themes from recent news
       - Impact on market sentiment
       - Potential catalysts identified

    4. Overall Assessment
       - Summary of findings
       - Risk factors
       - Trading recommendation (Buy/Hold/Sell)
       - Price targets (if applicable)
       - Key levels to watch
    """
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not Config.FMP_API_KEY:
            raise ValueError("FMP_API_KEY not found in environment variables") 