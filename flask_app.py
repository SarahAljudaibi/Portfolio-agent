from flask import Flask, render_template, request, jsonify
from portfolio_agent import PortfolioAgent
import os
import json
from datetime import datetime

app = Flask(__name__)

QA_LOG_FILE = "data/qa_log.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(QA_LOG_FILE):
    with open(QA_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_qa_log():
    if os.path.exists(QA_LOG_FILE):
        with open(QA_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_qa_log(entry):
    log = load_qa_log()
    log.append(entry)
    with open(QA_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

# Initialize the portfolio agent
try:
    agent = PortfolioAgent()
    print("Portfolio agent initialized successfully!")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

# In-memory conversation history per session
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    global conversation_history
    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': 'Please ask a question'})

        if not agent:
            return jsonify({'error': 'Portfolio agent is not available'})

        response = agent.answer_question(question, history=conversation_history)

        # Update in-memory history
        conversation_history.append({"question": question, "answer": response})

        # Save to JSON log
        save_qa_log({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "answer": response
        })

        return jsonify({'response': response})
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (Render.com requirement)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)