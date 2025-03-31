import React from 'react';
import Link from 'next/link';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { getRecentAnalyses } from '@/lib/stock-service';

export default function Home() {
  // Get recently analyzed stocks
  const recentAnalyses = getRecentAnalyses();
  
  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Stock Overview Card */}
        <div className="bg-gray-800 rounded-xl p-6 col-span-full lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Market Overview</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="text-sm text-gray-400">S&P 500</div>
              <div className="text-lg font-semibold">4,185.25</div>
              <div className="text-sm text-green-400">+1.25%</div>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="text-sm text-gray-400">NASDAQ</div>
              <div className="text-lg font-semibold">14,285.75</div>
              <div className="text-sm text-red-400">-0.75%</div>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="text-sm text-gray-400">DOW</div>
              <div className="text-lg font-semibold">32,845.20</div>
              <div className="text-sm text-green-400">+0.85%</div>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <div className="text-sm text-gray-400">VIX</div>
              <div className="text-lg font-semibold">18.25</div>
              <div className="text-sm text-red-400">-2.15%</div>
            </div>
          </div>
        </div>

        {/* Recent Analysis Card */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Analysis</h2>
          <div className="space-y-4">
            {recentAnalyses.map((analysis) => (
              <Link key={analysis.symbol} href={`/stock/${analysis.symbol}`} className="block">
                <div className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium">{analysis.symbol}</div>
                    <div className="text-sm text-gray-400">
                      {new Date(analysis.timestamp).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="text-sm text-gray-300">
                    {analysis.companyName}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Chart Section */}
        <div className="bg-gray-800 rounded-xl p-6 col-span-full lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Price Chart</h2>
          <div className="h-96 bg-gray-700 rounded-lg flex items-center justify-center">
            <span className="text-gray-400">Chart Component Coming Soon</span>
          </div>
        </div>

        {/* News Feed */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">Latest News</h2>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm font-medium mb-2">
                  Market Watch: Tech stocks lead the rally as AI boom continues
                </div>
                <div className="text-xs text-gray-400">2 hours ago • MarketWatch</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
} 