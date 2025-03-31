# StockSage AI - Financial News Analyzer

StockSage AI is an advanced financial analysis tool that combines the power of Agno's agent framework, Financial Modeling Prep's market data, and OpenAI's language models to provide comprehensive stock analysis and insights.

## 🗺️ Project Architecture

This project follows a client-server architecture with a clear separation of concerns:

```
financial_news_analyzer/
├── src/                     # Core Python backend for financial analysis
│   ├── main.py              # Entry point for the analyzer
│   ├── agents/              # Agent framework modules
│   ├── integrations/        # External API integrations
│   └── utils/               # Helper utilities
├── server.py                # Flask API server (middleware)
├── stocksage-dashboard/     # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js pages and routes
│   │   ├── components/      # React components
│   │   └── lib/             # Utility functions and services
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── analysis_results/        # Storage for analysis outputs
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

### Data Flow Architecture

The system works as follows:

1. **User Interface Layer** (Next.js)
   - User enters a stock symbol in the search bar
   - Dashboard displays analysis results and visualizations

2. **API Layer** (Flask)
   - Receives analysis requests from the frontend
   - Manages analyzed stocks data
   - Calls the financial analyzer backend

3. **Analysis Layer** (Python)
   - Fetches market data from Financial Modeling Prep API
   - Retrieves news from various sources
   - Uses OpenAI GPT-4 to analyze sentiment and generate insights
   - Calculates technical indicators
   - Produces comprehensive analysis output

4. **Storage Layer**
   - Analysis results are saved as JSON files

### Component Connections

- **Frontend → API**: The Next.js dashboard makes HTTP requests to the Flask API at http://localhost:5001/analyze and http://localhost:5001/stocks
- **API → Analyzer**: The Flask server executes the Python analyzer via subprocess
- **Analyzer → External APIs**: The Python backend connects to FMP API and OpenAI API
- **API → Storage**: Analysis results are saved to and loaded from the analysis_results directory

## 🚀 Features

- **Real-time Market Data Analysis**: Leverages Financial Modeling Prep API to fetch current market metrics
- **AI-Powered News Analysis**: Uses OpenAI's GPT-4 to analyze news sentiment and market trends
- **Technical Indicators**: Calculates key technical indicators like RSI and SMA
- **Beautiful Visualization**: Clean, responsive UI for displaying analysis results
- **Interactive Dashboard**: Web-based interface to search and analyze stocks

## 🛠️ Setup and Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Aary03/stocksage-ai.git
   cd stocksage-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   export OPENAI_API_KEY=your_key
   export FMP_API_KEY=your_key
   ```

5. Install Flask for the API server:
   ```bash
   pip install flask flask-cors
   ```

### Running the Backend

1. Start the Flask API server:
   ```bash
   python server.py
   ```

This will start the backend API server at http://localhost:5001.

### Frontend Setup

1. Navigate to the dashboard directory:
   ```bash
   cd stocksage-dashboard
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Frontend

1. Start the development server:
   ```bash
   npm run dev
   ```

This will start the Next.js app at http://localhost:3000.

## 📊 Using the Dashboard

1. Open http://localhost:3000 in your browser
2. Use the search bar to analyze a stock by symbol (e.g., AAPL, NFLX, TSLA)
3. Click "Analyze" to use the AI agent to analyze the stock
4. View detailed analysis including:
   - Market data
   - Technical indicators
   - News sentiment analysis
   - AI recommendations

## 🔌 API Endpoints

The backend provides these API endpoints:

- `POST /analyze`: Analyze a stock by symbol
  ```json
  {
    "symbol": "AAPL"
  }
  ```
  
  Response:
  ```json
  {
    "symbol": "AAPL",
    "market_data": {
      "price": 217.9,
      "change": -5.95,
      "change_percent": -2.65803,
      "volume": 39818617,
      "timestamp": "2025-03-31T13:02:29.380172",
      "high_52w": 260.1,
      "low_52w": 164.08,
      "market_cap": 3273315590000,
      "pe_ratio": 31.26
    },
    "technical_indicators": {
      "sma_50": 230.372,
      "rsi": 41.50
    },
    "news_analysis": {
      "items": [...],
      "sentiment_analysis": {
        "overall": 0.5
      }
    },
    "summary": "...",
    "risk_assessment": {
      "overall": "Moderate"
    },
    "recommendations": [
      "Hold"
    ]
  }
  ```

- `GET /stocks`: Get a list of all analyzed stocks
  
  Response:
  ```json
  [
    {
      "symbol": "AAPL",
      "timestamp": "2025-03-31T13:03:04.866158",
      "market_data": {
        "price": 217.9
      },
      "recommendation": "Hold"
    },
    ...
  ]
  ```

## 📦 Key Components

### Backend (Python)

1. **Financial News Analyzer**
   - Located in `src/main.py`
   - Uses Agno agent framework for orchestration
   - Makes API calls to fetch data and analyze stocks

2. **Flask API Server**
   - Located in `server.py`
   - Provides RESTful endpoints for the frontend
   - Handles running the analyzer process and returning results

### Frontend (Next.js + React)

1. **Dashboard Layout**
   - Components: `DashboardLayout.tsx`, `Header.tsx`, `Sidebar.tsx`
   - Provides the UI structure for the application

2. **Stock Service**
   - Located in `src/lib/stock-service.ts`
   - Handles communication with the backend API
   - Manages stock analysis data

3. **Pages**
   - Home page: Displays recent analyses and search functionality
   - Stock detail page: Shows comprehensive analysis for a specific stock

## 🏗️ Technology Stack

### Backend
- **Python 3.11+**: Core programming language
- **OpenAI API**: For AI analysis and natural language processing
- **Financial Modeling Prep API**: For market data
- **Flask**: For API server
- **Flask-CORS**: For cross-origin resource sharing

### Frontend
- **Next.js 14**: React framework for building the UI
- **React 18**: UI library
- **TypeScript**: For type-safe code
- **Tailwind CSS**: For styling
- **Recharts**: For data visualization

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📊 Implementation Plan

Future enhancements planned:
1. Add interactive charts with Recharts
2. Implement real-time price updates via WebSockets
3. Add portfolio tracking
4. Add alerts for price movements
5. Enhance the UI with responsive design for mobile

## 👥 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests. 

Market Data (FMP API) ─┐
News Articles ─────────┼─► Agno Agent ─► OpenAI Analysis ─► Final Report
Technical Indicators ──┘ 