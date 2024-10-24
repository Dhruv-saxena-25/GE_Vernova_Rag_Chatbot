from flask import Flask, render_template, request, session
from src.retriever import retrieval
from src.fetch_doc import extract_pdf_pages_as_images_base64
import uuid

app = Flask(__name__)
app.secret_key = 'unique'  # Needed for session handling


def generate_session_id():
    """Generate a unique session ID."""
    return str(uuid.uuid4())


@app.before_request
def manage_session():
    """Ensure that each session has a unique ID and history."""
    if 'session_id' not in session:
        # Generate a new session ID and start a new chat history
        session['session_id'] = generate_session_id()
        session['chat_history'] = []


@app.route('/')
def home():
    return render_template('new_home.html')


@app.route('/pdf_chat', methods=['GET', 'POST'])
def pdf_chat():
    return render_template('new_chat.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    images_base64 = []

    if request.method == 'POST':
        user_question = request.form['user_question']
        result, page_number = retrieval(user_question)
        response = result["answer"]

        # Extract images for the relevant pages
        images_base64 = extract_pdf_pages_as_images_base64(page_number)
        
        # Append the user's question and the bot's response to chat history
        session['chat_history'].append({'content': f'User: {user_question}'})
        session['chat_history'].append({'content': f'Bot: {response}'})

    # Retrieve the entire chat history and images from the session
    chat_history = session.get('chat_history', [])
    
    return render_template('new_chat.html', chat_history=chat_history, images_base64=images_base64)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
