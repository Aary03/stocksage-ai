import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from ..config import Config
from ..utils.logger import logger

class FMPService:
    """Service class for Financial Modeling Prep API calls"""
    
    def __init__(self):
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.api_key = Config.FMP_API_KEY
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get current quote data for a symbol"""
        try:
            url = f"{self.base_url}/quote/{symbol}?apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data[0] if data else {}
        except Exception as e:
            logger.error(f"Error fetching quote data for {symbol}: {str(e)}")
            raise
    
    def get_sma(self, symbol: str, period: int = 50) -> Optional[float]:
        """Get Simple Moving Average (SMA) for a symbol"""
        try:
            url = f"{self.base_url}/technical_indicator/daily/{symbol}?period={period}&type=sma&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data[0]['sma'] if data else None
        except Exception as e:
            logger.error(f"Error fetching SMA data for {symbol}: {str(e)}")
            raise
    
    def get_rsi(self, symbol: str, period: int = 14) -> Optional[float]:
        """Get Relative Strength Index (RSI) for a symbol"""
        try:
            url = f"{self.base_url}/technical_indicator/daily/{symbol}?period={period}&type=rsi&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data[0]['rsi'] if data else None
        except Exception as e:
            logger.error(f"Error fetching RSI data for {symbol}: {str(e)}")
            raise
    
    def get_news(self, symbol: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get news articles for a symbol"""
        try:
            url = f"{self.base_url}/stock_news?tickers={symbol}&limit={limit}&apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching news data for {symbol}: {str(e)}")
            raise 