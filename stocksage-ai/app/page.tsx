'use client';

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface MarketData {
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  high_52w: number;
  low_52w: number;
  market_cap: number;
  pe_ratio: number;
}

interface TechnicalIndicators {
  sma_50: number;
  rsi: number;
}

interface NewsItem {
  title: string;
  source: string;
  published_date: string;
  sentiment_score: number;
}

interface StockAnalysis {
  symbol: string;
  market_data: MarketData;
  technical_indicators: TechnicalIndicators;
  news_analysis: {
    items: NewsItem[];
    sentiment_analysis: {
      overall: number;
    };
  };
  summary: string;
  risk_assessment: {
    overall: string;
  };
  recommendations: string[];
}

export default function Home() {
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<StockAnalysis | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/analyze?symbol=${symbol}`);
      const data = await response.json();
      setAnalysis(data);
    } catch (error) {
      console.error('Error analyzing stock:', error);
    }
    setLoading(false);
  };

  return (
    <main className="container mx-auto px-4">
      <div className="flex flex-col items-center justify-center min-h-[200px] text-center">
        <h1 className="text-4xl font-bold mb-8 text-gray-800 dark:text-white">
          Intelligent Stock Analysis
        </h1>
        <div className="flex gap-4 w-full max-w-md">
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="Enter stock symbol (e.g., AAPL)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleAnalyze}
            disabled={loading || !symbol}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>

      {analysis && (
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Market Data Card */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Market Data</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">Price</p>
                <p className="text-xl font-bold text-gray-800 dark:text-white">${analysis.market_data.price}</p>
              </div>
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">Change</p>
                <p className={`text-xl font-bold ${analysis.market_data.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {analysis.market_data.change_percent.toFixed(2)}%
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">Volume</p>
                <p className="text-xl font-bold text-gray-800 dark:text-white">
                  {analysis.market_data.volume.toLocaleString()}
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">Market Cap</p>
                <p className="text-xl font-bold text-gray-800 dark:text-white">
                  ${(analysis.market_data.market_cap / 1e9).toFixed(2)}B
                </p>
              </div>
            </div>
          </div>

          {/* Technical Indicators Card */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Technical Indicators</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">50-day SMA</p>
                <p className="text-xl font-bold text-gray-800 dark:text-white">
                  ${analysis.technical_indicators.sma_50.toFixed(2)}
                </p>
              </div>
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-500 dark:text-gray-400">RSI</p>
                <p className="text-xl font-bold text-gray-800 dark:text-white">
                  {analysis.technical_indicators.rsi.toFixed(2)}
                </p>
              </div>
            </div>
          </div>

          {/* News Analysis Card */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg md:col-span-2">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Latest News</h2>
            <div className="space-y-4">
              {analysis.news_analysis.items.map((item, index) => (
                <div key={index} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h3 className="font-semibold text-gray-800 dark:text-white">{item.title}</h3>
                  <div className="flex justify-between mt-2 text-sm text-gray-500 dark:text-gray-400">
                    <span>{item.source}</span>
                    <span>{new Date(item.published_date).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Summary Card */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg md:col-span-2">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Analysis Summary</h2>
            <div className="prose dark:prose-invert max-w-none">
              <div className="whitespace-pre-wrap text-gray-600 dark:text-gray-300">
                {analysis.summary}
              </div>
            </div>
          </div>

          {/* Recommendations Card */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg md:col-span-2">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Recommendations</h2>
            <div className="flex gap-4 flex-wrap">
              {analysis.recommendations.map((rec, index) => (
                <div
                  key={index}
                  className="px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100 rounded-full font-semibold"
                >
                  {rec}
                </div>
              ))}
              <div className="px-4 py-2 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-100 rounded-full font-semibold">
                Risk: {analysis.risk_assessment.overall}
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
} 