from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class NewsItem:
    title: str
    content: str
    source: str
    published_date: datetime
    url: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_magnitude: Optional[float] = None
    keywords: List[str] = field(default_factory=list)
    
@dataclass
class MarketData:
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert market data to dictionary format"""
        return {
            'symbol': self.symbol,
            'price': self.price,
            'change': self.change,
            'change_percent': self.change_percent,
            'volume': self.volume,
            'timestamp': self.timestamp.isoformat(),
            'high_52w': self.high_52w,
            'low_52w': self.low_52w,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio
        }
    
@dataclass
class TechnicalIndicators:
    sma_50: Optional[float] = None
    rsi: Optional[float] = None

    def to_dict(self) -> Dict:
        """Convert technical indicators to dictionary format"""
        return {
            'sma_50': self.sma_50,
            'rsi': self.rsi
        }

@dataclass
class FinancialAnalysis:
    symbol: str
    market_data: MarketData
    technical_indicators: TechnicalIndicators
    news_items: List[NewsItem]
    summary: str
    sentiment_analysis: Dict[str, float]
    risk_assessment: Dict[str, str]
    recommendations: List[str]
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert analysis to dictionary format"""
        return {
            'symbol': self.symbol,
            'market_data': {
                'price': self.market_data.price,
                'change': self.market_data.change,
                'change_percent': self.market_data.change_percent,
                'volume': self.market_data.volume,
                'timestamp': self.market_data.timestamp.isoformat(),
                'high_52w': self.market_data.high_52w,
                'low_52w': self.market_data.low_52w,
                'market_cap': self.market_data.market_cap,
                'pe_ratio': self.market_data.pe_ratio
            },
            'technical_indicators': {
                'sma_50': self.technical_indicators.sma_50,
                'rsi': self.technical_indicators.rsi
            },
            'news_analysis': {
                'items': [
                    {
                        'title': item.title,
                        'source': item.source,
                        'published_date': item.published_date.isoformat(),
                        'sentiment_score': item.sentiment_score,
                        'sentiment_magnitude': item.sentiment_magnitude,
                        'keywords': item.keywords
                    } for item in self.news_items
                ],
                'sentiment_analysis': self.sentiment_analysis
            },
            'summary': self.summary,
            'risk_assessment': self.risk_assessment,
            'recommendations': self.recommendations,
            'analysis_timestamp': self.analysis_timestamp.isoformat()
        } 