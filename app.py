from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'flashcard_db')
}

# Initialize database
def init_db():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
    cursor.execute(f"USE {db_config['database']}")
    
    # Create flashcards table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
HF_API_TOKEN = os.getenv('HF_API_TOKEN')  # You'll need to get this from Hugging Face

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-flashcards', methods=['POST'])
def generate_flashcards():
    try:
        text = request.json.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # For a hackathon, we'll simulate question generation
        # In a real scenario, you'd use the Hugging Face API
        questions_answers = simulate_question_generation(text)
        
        # Save to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        for qa in questions_answers:
            cursor.execute(
                "INSERT INTO flashcards (question, answer) VALUES (%s, %s)",
                (qa['question'], qa['answer'])
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'flashcards': questions_answers})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def simulate_question_generation(text):
    # This is a simulation for the hackathon
    # In a real application, you would use the Hugging Face API
    # For example:
    # payload = {"inputs": text}
    # response = requests.post(HF_API_URL, headers=headers, json=payload)
    # Process the response to extract questions and answers
    
    # Simulated response for demonstration
    samples = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}
    ]
    
    return samples

@app.route('/get-flashcards', methods=['GET'])
def get_flashcards():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM flashcards ORDER BY created_at DESC")
        flashcards = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({'flashcards': flashcards})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)