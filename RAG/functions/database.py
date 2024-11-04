# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_message(role, content):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages ORDER BY timestamp')
    messages = cursor.fetchall()
    conn.close()
    print(f"Messages retrieved from database: {messages}") 
    return messages

def get_messages_dict():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages ORDER BY timestamp')
    messages = cursor.fetchall()
    conn.close()
    
    # Convertendo a lista de tuplas em uma lista de dicionários
    messages_list = [{'role': role, 'content': content} for role, content in messages]
    
    print(f"Messages retrieved from database: {messages_list}") 
    return messages_list