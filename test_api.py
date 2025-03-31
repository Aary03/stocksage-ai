import requests
import json

def test_analyze_endpoint():
    """Test the /analyze endpoint with a known stock symbol."""
    url = "http://localhost:5001/analyze"
    payload = {"symbol": "AAPL"}
    
    print(f"Testing analyze endpoint with {payload}...")
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Analysis successful!")
            print(f"Symbol: {data.get('symbol')}")
            
            # Print market data if available
            market_data = data.get('market_data', {})
            if market_data:
                print(f"Price: ${market_data.get('price', 'N/A')}")
                print(f"Change: {market_data.get('change_percent', 'N/A')}%")
            
            # Print recommendation if available
            recommendations = data.get('recommendations', [])
            if recommendations:
                print(f"Recommendation: {recommendations[0]}")
        else:
            print(f"Error: {response.json()}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_stocks_endpoint():
    """Test the /stocks endpoint to get a list of analyzed stocks."""
    url = "http://localhost:5001/stocks"
    
    print("\nTesting stocks endpoint...")
    
    try:
        response = requests.get(url)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            stocks = response.json()
            print(f"Found {len(stocks)} analyzed stocks:")
            
            for i, stock in enumerate(stocks, 1):
                print(f"{i}. {stock.get('symbol')} - {stock.get('timestamp', 'N/A')}")
        else:
            print(f"Error: {response.json()}")
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("API Test Script")
    print("==============")
    
    test_analyze_endpoint()
    test_stocks_endpoint()
    
    print("\nTests completed.") 