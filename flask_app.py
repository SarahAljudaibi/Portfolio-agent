from flask import Flask, render_template, request, jsonify
from portfolio_agent import PortfolioAgent
import os

app = Flask(__name__)

# Initialize the portfolio agent
try:
    agent = PortfolioAgent()
    print("Portfolio agent initialized successfully!")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Please ask a question'})
        
        if not agent:
            return jsonify({'error': 'Portfolio agent is not available'})
        
        response = agent.answer_question(question)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (Render.com requirement)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)