'use client';

import React from 'react';
import Link from 'next/link';

const watchlistItems = [
  { symbol: 'AAPL', name: 'Apple Inc.' },
  { symbol: 'NFLX', name: 'Netflix Inc.' },
  { symbol: 'CELH', name: 'Celsius Holdings' },
  { symbol: 'TSLA', name: 'Tesla Inc.' },
];

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-800 p-6 flex flex-col">
      {/* Logo */}
      <div className="mb-8">
        <h1 className="text-xl font-bold text-white">StockSage AI</h1>
      </div>

      {/* Navigation */}
      <nav className="mb-8">
        <ul className="space-y-2">
          <li>
            <Link href="/" className="text-gray-300 hover:text-white">
              Dashboard
            </Link>
          </li>
          <li>
            <Link href="/portfolio" className="text-gray-300 hover:text-white">
              Portfolio
            </Link>
          </li>
          <li>
            <Link href="/alerts" className="text-gray-300 hover:text-white">
              Alerts
            </Link>
          </li>
        </ul>
      </nav>

      {/* Watchlist */}
      <div className="flex-1">
        <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Watchlist</h2>
        <ul className="space-y-3">
          {watchlistItems.map((item) => (
            <li key={item.symbol}>
              <Link 
                href={`/stock/${item.symbol}`}
                className="block p-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
              >
                <div className="font-medium">{item.symbol}</div>
                <div className="text-sm text-gray-400">{item.name}</div>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
} 