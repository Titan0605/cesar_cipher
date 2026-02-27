from flask import Flask, request, jsonify
from enum import Enum

class Alphabet(Enum):
    ENGLISH = "abcdefghijklmnopqrstuvwxyz"
    SPANISH = "abcdefghijklmnñopqrstuvwxyz"

class CesarCipher:
    def __init__(self) -> None:
        pass
    
    def encrypt(self, text: str, shift: int, alphabet: Alphabet) -> str:
        result = []
        alphabet_length = len(alphabet.value)
        
        for char in text:
            char_index = alphabet.value.find(char.lower())
            
            if char_index == -1: # When find() doesn't find the char, appends the exact char 
                result.append(char)
                continue
            
            new_char = alphabet.value[(char_index + shift) % alphabet_length]
            # Preserve uppercase if the original character was uppercase
            result.append(new_char.upper() if char.isupper() else new_char)
            
        return "".join(result)
    
    def decrypt(self, text: str, shift: int, alphabet: Alphabet) -> str:
        result = []
        alphabet_length = len(alphabet.value)
        
        for char in text:
            char_index = alphabet.value.find(char.lower())
            
            if char_index == -1: # When find() doesn't find the char, appends the exact char 
                result.append(char)
                continue
            
            new_char = alphabet.value[(char_index - shift) % alphabet_length]
            # Preserve uppercase if the original character was uppercase
            result.append(new_char.upper() if char.isupper() else new_char)
            
        return "".join(result)


cipher = CesarCipher()

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)