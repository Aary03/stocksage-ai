from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze a stock symbol using the financial news analyzer."""
    data = request.json
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400
    
    try:
        # Log the request
        print(f"Analyzing stock: {symbol}")
        
        # Use the output directory for analysis results
        output_dir = 'analysis_results'
        os.makedirs(output_dir, exist_ok=True)
        
        # Run the financial news analyzer as a subprocess
        # Replace this with the actual command to run your analyzer
        cmd = ['python', '-m', 'src.main', symbol, '-o', output_dir]
        
        # Run the command and capture output
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error analyzing stock: {stderr}")
            return jsonify({'error': f'Failed to analyze stock: {stderr}'}), 500
            
        # Read the analysis results from the output file
        result_file = os.path.join(output_dir, f"{symbol}_analysis.json")
        
        # Check if the file exists
        if not os.path.exists(result_file):
            return jsonify({'error': 'Analysis failed to generate results'}), 500
            
        with open(result_file, 'r') as f:
            analysis = json.load(f)
            
        return jsonify(analysis)
        
    except Exception as e:
        print(f"Error analyzing stock: {str(e)}")
        return jsonify({'error': f'Failed to analyze stock: {str(e)}'}), 500

@app.route('/stocks', methods=['GET'])
def get_analyzed_stocks():
    """Get a list of all analyzed stocks."""
    try:
        output_dir = 'analysis_results'
        
        if not os.path.exists(output_dir):
            return jsonify([])
            
        # Get all JSON files in the output directory
        files = [f for f in os.listdir(output_dir) if f.endswith('_analysis.json')]
        
        stocks = []
        for file in files:
            symbol = file.replace('_analysis.json', '')
            
            with open(os.path.join(output_dir, file), 'r') as f:
                data = json.load(f)
                
            stocks.append({
                'symbol': symbol,
                'companyName': data.get('company_name', f"{symbol} Inc."),
                'timestamp': data.get('analysis_timestamp', datetime.now().isoformat())
            })
            
        return jsonify(stocks)
        
    except Exception as e:
        print(f"Error getting analyzed stocks: {str(e)}")
        return jsonify({'error': f'Failed to get analyzed stocks: {str(e)}'}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True) 