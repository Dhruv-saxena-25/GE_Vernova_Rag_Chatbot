from flask import Flask, render_template, request, redirect, session
from src.retriever import retrieval

# Flask App
app = Flask(__name__)
app.secret_key = 'dhruv'  # Needed for session handling

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pdf_chat', methods=['GET', 'POST'])
def pdf_chat():
    return render_template('chat.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # Initialize chat history in session if not already present
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if request.method == 'POST':
        user_question = request.form['user_question']
        response = retrieval(user_question)
        
        # Append the user's question and response to chat history
        session['chat_history'].append({'content': f'User: {user_question}'})
        session['chat_history'].append({'content': f'Bot: {response}'})
    
    # Retrieve chat history from session
    chat_history = session.get('chat_history', [])
    
    return render_template('chat.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
