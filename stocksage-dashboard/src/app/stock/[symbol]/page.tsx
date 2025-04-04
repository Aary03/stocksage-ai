'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { getStockAnalysis, analyzeStock, StockAnalysis } from '@/lib/stock-service';

interface StockDetailProps {
  params: {
    symbol: string;
  };
}

export default function StockDetail({ params }: StockDetailProps) {
  const { symbol } = params;
  const [stockData, setStockData] = useState<StockAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if we already have data for this stock
    const existingData = getStockAnalysis(symbol);
    if (existingData) {
      setStockData(existingData);
    }

    // If not, show the analysis request UI
  }, [symbol]);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // This would call your backend API in a real implementation
      const result = await analyzeStock(symbol);
      
      if (result) {
        setStockData(result);
      } else {
        setError(`Could not analyze ${symbol}. Please check the symbol and try again.`);
      }
    } catch (err) {
      setError(`Error analyzing stock: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };
  
  // If no data is found and not currently analyzing, show request analysis UI
  if (!stockData && !loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center py-16">
          <h1 className="text-2xl font-semibold mb-6">Analyze {symbol}</h1>
          
          {error && (
            <div className="mb-6 bg-red-900/30 border border-red-700 text-red-100 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <p className="text-gray-400 mb-8 text-center max-w-md">
            No existing analysis found for {symbol}. Would you like to generate a new analysis using the StockSage AI agent?
          </p>
          
          <button 
            onClick={handleAnalyze}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
          >
            Analyze {symbol}
          </button>
        </div>
      </DashboardLayout>
    );
  }

  // Show loading state
  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center py-16">
          <h1 className="text-2xl font-semibold mb-6">Analyzing {symbol}...</h1>
          <div className="animate-pulse flex space-x-4">
            <div className="rounded-full bg-gray-700 h-12 w-12"></div>
            <div className="flex-1 space-y-4 py-1">
              <div className="h-4 bg-gray-700 rounded w-3/4"></div>
              <div className="space-y-2">
                <div className="h-4 bg-gray-700 rounded"></div>
                <div className="h-4 bg-gray-700 rounded w-5/6"></div>
              </div>
            </div>
          </div>
          <p className="text-gray-400 mt-6">
            StockSage AI is analyzing market data, technical indicators, and news sentiment...
          </p>
        </div>
      </DashboardLayout>
    );
  }
  
  // If we have stock data, show it
  if (!stockData) {
    return null; // This shouldn't happen but TypeScript needs this check
  }
  
  return (
    <DashboardLayout>
      <div className="mb-6">
        <div className="flex items-baseline gap-2">
          <h1 className="text-3xl font-bold">{stockData.symbol}</h1>
          <span className="text-xl text-gray-400">{stockData.companyName}</span>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Price Overview */}
        <div className="bg-gray-800 rounded-xl p-6 lg:col-span-2">
          <div className="flex items-start justify-between mb-6">
            <div>
              <span className="text-4xl font-bold">${stockData.marketData.price.toFixed(2)}</span>
              <span className={`ml-3 text-xl ${stockData.marketData.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {stockData.marketData.change >= 0 ? '+' : ''}{stockData.marketData.change.toFixed(2)} ({stockData.marketData.changePercent.toFixed(2)}%)
              </span>
            </div>
            <div className={`px-4 py-1.5 rounded-full font-medium ${
              stockData.recommendation === 'Buy' ? 'bg-green-500/20 text-green-400' : 
              stockData.recommendation === 'Hold' ? 'bg-yellow-500/20 text-yellow-400' : 
              'bg-red-500/20 text-red-400'
            }`}>
              {stockData.recommendation}
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            <div>
              <div className="text-sm text-gray-400">Volume</div>
              <div className="text-lg font-medium">{stockData.marketData.volume.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Market Cap</div>
              <div className="text-lg font-medium">${(stockData.marketData.marketCap / 1000000000).toFixed(2)}B</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">P/E Ratio</div>
              <div className="text-lg font-medium">{stockData.marketData.peRatio.toFixed(2)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">50-day SMA</div>
              <div className="text-lg font-medium">${stockData.technicalIndicators.sma50.toFixed(2)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">RSI</div>
              <div className="text-lg font-medium">{stockData.technicalIndicators.rsi.toFixed(2)}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Risk Level</div>
              <div className="text-lg font-medium">{stockData.riskAssessment}</div>
            </div>
          </div>
        </div>
        
        {/* AI Insights */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">AI Insights</h2>
          <div className="space-y-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="font-medium mb-2">Technical Analysis</div>
              <div className="text-sm text-gray-300">
                Bullish momentum with strong technical indicators. RSI at {stockData.technicalIndicators.rsi.toFixed(2)} suggests room for growth but approaching overbought levels.
              </div>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="font-medium mb-2">Sentiment Analysis</div>
              <div className="text-sm text-gray-300">
                Recent news has been overwhelmingly positive, focusing on profit potential and long-term growth prospects.
              </div>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="font-medium mb-2">Valuation Assessment</div>
              <div className="text-sm text-gray-300">
                High P/E ratio of {stockData.marketData.peRatio.toFixed(2)} suggests premium valuation. Future growth expectations are built into the current price.
              </div>
            </div>
          </div>
        </div>
        
        {/* Price Chart */}
        <div className="bg-gray-800 rounded-xl p-6 lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Price Chart</h2>
          <div className="h-96 bg-gray-700 rounded-lg flex items-center justify-center">
            <span className="text-gray-400">Interactive Chart Coming Soon</span>
          </div>
        </div>
        
        {/* News Feed */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">Latest News</h2>
          <div className="space-y-4">
            {stockData.newsItems.map((news, index) => (
              <div key={index} className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm font-medium mb-2">{news.title}</div>
                <div className="text-xs text-gray-400">
                  {new Date(news.publishedDate).toLocaleDateString()} • {news.source}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Full Analysis */}
        <div className="bg-gray-800 rounded-xl p-6 col-span-full">
          <h2 className="text-xl font-semibold mb-4">Full Analysis</h2>
          <div className="bg-gray-700 rounded-lg p-6 text-gray-300 text-sm">
            <p className="whitespace-pre-line">{stockData.summary}</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
} 