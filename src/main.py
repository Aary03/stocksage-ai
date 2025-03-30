import argparse
import json
import os
import asyncio
from typing import Optional

from src.agents.financial_agent import FinancialNewsAgent
from src.utils.logger import logger

async def analyze_stock(symbol: str, output_dir: Optional[str] = None) -> None:
    """Run stock analysis"""
    try:
        # Initialize agent
        agent = FinancialNewsAgent()
        
        # Perform analysis
        analysis = await agent.analyze_stock(symbol)
        
        # Print summary
        logger.info("\nAnalysis Summary:")
        logger.info(f"Symbol: {analysis.symbol}")
        logger.info(f"Current Price: ${analysis.market_data.price:.2f}")
        logger.info(f"Change: ${analysis.market_data.change:.2f} ({analysis.market_data.change_percent:.2f}%)")
        logger.info(f"Volume: {analysis.market_data.volume:,}")
        logger.info(f"52-Week Range: ${analysis.market_data.low_52w:.2f} - ${analysis.market_data.high_52w:.2f}")
        logger.info(f"Market Cap: ${analysis.market_data.market_cap:,}")
        logger.info(f"P/E Ratio: {analysis.market_data.pe_ratio:.2f}")
        logger.info(f"\nTechnical Indicators:")
        logger.info(f"50-day SMA: ${analysis.technical_indicators.sma_50:.2f}")
        logger.info(f"RSI: {analysis.technical_indicators.rsi:.2f}")
        logger.info(f"\nRecommendations: {', '.join(analysis.recommendations)}")
        logger.info(f"Risk Assessment: {analysis.risk_assessment['overall']}")
        logger.info(f"\nSummary:")
        logger.info(analysis.summary)
        
        # Save results if output directory specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{symbol}_analysis.json")
            with open(output_file, 'w') as f:
                json.dump(analysis.to_dict(), f, indent=2)
            logger.info(f"\nAnalysis saved to {output_file}")
            
    except Exception as e:
        logger.error(f"Error analyzing stock {symbol}: {str(e)}")
        raise

def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Financial News Analyzer')
    parser.add_argument('symbol', help='Stock symbol to analyze')
    parser.add_argument('-o', '--output', help='Output directory for analysis results')
    args = parser.parse_args()
    
    # Run analysis
    try:
        asyncio.run(analyze_stock(args.symbol, args.output))
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()