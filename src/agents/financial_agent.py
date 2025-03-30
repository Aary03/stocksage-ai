from typing import List, Dict, Optional
import requests
from datetime import datetime, timedelta
from textblob import TextBlob

from ..core.base_agent import BaseAgent
from ..core.models import NewsItem, MarketData, TechnicalIndicators, FinancialAnalysis
from ..config import Config
from ..utils.logger import logger
from ..services.fmp_service import FMPService

class FinancialNewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Financial News Analyzer",
            role="Expert financial analyst specializing in market analysis and news interpretation",
            instructions=[
                "Analyze financial news and market data to provide comprehensive insights",
                "Evaluate market sentiment and technical indicators",
                "Generate actionable trading recommendations",
                "Identify key market trends and potential risks",
                "Provide clear and concise analysis summaries"
            ]
        )
        self.fmp_service = FMPService()
        
    async def analyze_stock(self, symbol: str) -> FinancialAnalysis:
        """Analyze a stock and generate insights"""
        try:
            logger.info(f"Starting analysis for {symbol}")
            
            # Get market data
            market_data = self._get_market_data(symbol)
            technical_indicators = self._calculate_technical_indicators(symbol)
            news_items = self._analyze_news(symbol)
            
            # Create analysis prompt
            analysis_prompt = self._create_analysis_prompt(
                symbol, market_data, technical_indicators, news_items
            )
            
            # Get analysis from LLM
            analysis_response = await self.execute(analysis_prompt)
            
            # Create final analysis object
            analysis = FinancialAnalysis(
                symbol=symbol,
                market_data=market_data,
                technical_indicators=technical_indicators,
                news_items=news_items,
                summary=analysis_response,
                sentiment_analysis={'overall': 0.5},  # Default sentiment
                risk_assessment={'overall': 'Moderate'},  # Default risk assessment
                recommendations=['Hold']  # Default recommendation
            )
            
            logger.info(f"Completed analysis for {symbol}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing stock {symbol}: {str(e)}")
            raise
            
    def _get_market_data(self, symbol: str) -> MarketData:
        """Get market data for a stock"""
        try:
            data = self.fmp_service.get_quote(symbol)
            return MarketData(
                symbol=symbol,
                price=data["price"],
                change=data["change"],
                change_percent=data["changesPercentage"],
                volume=data["volume"],
                timestamp=datetime.now(),
                high_52w=data["yearHigh"],
                low_52w=data["yearLow"],
                market_cap=data["marketCap"],
                pe_ratio=data["pe"]
            )
        except Exception as e:
            logger.error(f"Error getting market data: {str(e)}")
            raise
            
    def _calculate_technical_indicators(self, symbol: str) -> TechnicalIndicators:
        """Calculate technical indicators for a stock"""
        try:
            sma_50 = self.fmp_service.get_sma(symbol, 50)
            rsi = self.fmp_service.get_rsi(symbol)
            return TechnicalIndicators(
                sma_50=sma_50,
                rsi=rsi
            )
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            raise
            
    def _analyze_news(self, symbol: str) -> List[NewsItem]:
        """Get and analyze news for a stock"""
        try:
            news_data = self.fmp_service.get_news(symbol)
            news_items = []
            for item in news_data:
                news_items.append(NewsItem(
                    title=item["title"],
                    content=item["text"],
                    source=item["site"],
                    published_date=datetime.strptime(item["publishedDate"], "%Y-%m-%d %H:%M:%S"),
                    url=item["url"],
                    sentiment_score=0.5,  # Default sentiment score
                    sentiment_magnitude=0.5,  # Default sentiment magnitude
                    keywords=[]  # Empty keywords list for now
                ))
            return news_items
        except Exception as e:
            logger.error(f"Error analyzing news: {str(e)}")
            raise
            
    def _create_analysis_prompt(
        self,
        symbol: str,
        market_data: MarketData,
        technical_indicators: TechnicalIndicators,
        news_items: List[NewsItem]
    ) -> str:
        """Create a prompt for the agent to analyze the data"""
        # Unpack market data
        market_dict = market_data.to_dict()
        # Unpack technical indicators
        tech_dict = technical_indicators.to_dict()
        
        # Format the prompt with all variables
        return Config.ANALYSIS_PROMPT_TEMPLATE.format(
            symbol=symbol,
            price=market_dict['price'],
            change=market_dict['change'],
            change_percent=market_dict['change_percent'],
            volume=market_dict['volume'],
            high_52w=market_dict['high_52w'],
            low_52w=market_dict['low_52w'],
            market_cap=market_dict['market_cap'],
            pe_ratio=market_dict['pe_ratio'],
            sma_50=tech_dict['sma_50'],
            rsi=tech_dict['rsi'],
            news_summary=self._summarize_news(news_items)
        )
        
    def _calculate_overall_sentiment(self, news_items: List[NewsItem]) -> float:
        """Calculate overall sentiment from news items"""
        if not news_items:
            return 0.0
            
        total_score = sum(item.sentiment_score for item in news_items)
        return total_score / len(news_items)
        
    def _assess_risk(
        self,
        market_data: MarketData,
        technical_indicators: TechnicalIndicators
    ) -> str:
        """Assess risk level based on market data and technical indicators"""
        risk_factors = []
        
        # Check price relative to moving average
        if market_data.price < technical_indicators.sma_50:
            risk_factors.append("Price below 50-day SMA")
            
        # Check RSI
        if technical_indicators.rsi > 70:
            risk_factors.append("RSI indicates overbought")
        elif technical_indicators.rsi < 30:
            risk_factors.append("RSI indicates oversold")
            
        # Assess volatility
        if market_data.change_percent and abs(market_data.change_percent) > 5:
            risk_factors.append("High daily volatility")
            
        if not risk_factors:
            return "Low risk - No significant risk factors identified"
        elif len(risk_factors) == 1:
            return f"Moderate risk - {risk_factors[0]}"
        else:
            return f"High risk - Multiple factors: {', '.join(risk_factors)}"
            
    def _generate_recommendations(self, analysis: str) -> List[str]:
        """Generate recommendations based on the analysis"""
        # This could be enhanced with more sophisticated logic
        recommendations = []
        
        if "bullish" in analysis.lower():
            recommendations.append("Consider long positions with appropriate stop-loss")
        if "bearish" in analysis.lower():
            recommendations.append("Consider reducing exposure or implementing hedges")
        if "volatile" in analysis.lower():
            recommendations.append("Monitor position sizes and use strict risk management")
            
        if not recommendations:
            recommendations.append("Maintain current positions and monitor market conditions")
            
        return recommendations
        
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        blob = TextBlob(text)
        return [phrase.string for phrase in blob.noun_phrases]
        
    def _summarize_news(self, news_items: List[NewsItem]) -> str:
        """Create a summary of news items"""
        if not news_items:
            return "No recent news available."
            
        summary = []
        for item in news_items:
            pub_date = item.published_date.strftime('%Y-%m-%d')
            sentiment = "positive" if item.sentiment_score > 0.1 else "negative" if item.sentiment_score < -0.1 else "neutral"
            summary.append(f"- [{pub_date}] {item.title} (Source: {item.source}, Sentiment: {sentiment})")
            
        return "\n".join(summary) 