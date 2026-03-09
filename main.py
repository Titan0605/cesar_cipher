from flask import Flask, request, jsonify, g
from werkzeug import security
import sqlite3 as sql

from classes import CesarCipher
from enums import Alphabet
from utils.db import init_db, get_db

DB_PATH = 'users.db'
CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY NOT NULL,
        password_hash TEXT NOT NULL
    )
'''

cipher = CesarCipher()
app = Flask(__name__)
    
@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

with app.app_context():
    init_db(DB_PATH, CREATE_USERS_TABLE)

def get_alphabet(alphabet_key: int) -> Alphabet:
    match alphabet_key:
        case 2:
            return Alphabet.SPANISH
        case _:
            return Alphabet.ENGLISH

@app.route('/api/encrypt', methods=['POST'])
def encrypt_endpoint():
    data = request.get_json()
    
    text = data.get('text', '')
    shift = data.get('shift', 0)
    alphabet_key = data.get('alphabet', 1)  # 1 = English, 2 = Spanish

    selected_alphabet = get_alphabet(alphabet_key)
    result = cipher.encrypt(text, shift, selected_alphabet)

    return jsonify({'result': result})

@app.route('/api/decrypt', methods=['POST'])
def decrypt_endpoint():
    data = request.get_json()
    text = data.get('text', '')
    shift = data.get('shift', 0)
    alphabet_key = data.get('alphabet', 1)  # 1 = English, 2 = Spanish

    selected_alphabet = get_alphabet(alphabet_key)
    result = cipher.decrypt(text, shift, selected_alphabet)

    return jsonify({'result': result})

@app.route('/api/register', methods=['POST'])
def register_endpoint():
    data = request.get_json()
    
    username = data.get('username', '')
    password = data.get('password', '')
    
    db = get_db(DB_PATH)

    row = db.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone()

    if row is not None:
        return jsonify({'message': 'User already exists', 'status': '409'})
    
    db.execute(
        'INSERT INTO users (username, password_hash) VALUES (?, ?)',
        (username, security.generate_password_hash(password))
    )
    db.commit()
    
    return jsonify({'message': 'User registered', 'status': '201'})

@app.route('/api/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()
    
    username = data.get('username', '')
    password = data.get('password', '')
    
    db = get_db(DB_PATH)
    
    row = db.execute('SELECT password_hash AS hash FROM users WHERE username = ?', (username,)).fetchone()
    
    if row is None:
        return jsonify({'message': 'User doesn\'t exists', 'status': '404'})
    
    if not security.check_password_hash(row['hash'], password):
        return jsonify({'message': 'Incorrect credentials', 'status': '401'})
    
    return jsonify({'message': 'Login succesful', 'status': '200'})

if __name__ == "__main__":
    app.run(debug=True)