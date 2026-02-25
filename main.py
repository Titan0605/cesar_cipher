import sys
from enum import Enum

class Alphabet(Enum):
    ENGLISH = "abcdefghijklmnopqrstuvwxyz"
    SPANISH = "abcdefghijklmnñopqrstuvwxyz"

class CesarCipher:
    def __init__(self) -> None:
        pass
    
    def encrypt(self, text: str, shift: str, alphabet: Alphabet) -> str:
        result = []
        alphabet_length = len(alphabet.value)
        
        for char in text:
            char_index = alphabet.value.find(char.lower())
            
            if char_index == -1: # When find() doesn't find the char, appends the exact char 
                result.append(char)
                continue
            
            new_char = alphabet.value[(char_index + int(shift)) % alphabet_length]
            # Preserve uppercase if the original character was uppercase
            result.append(new_char.upper() if char.isupper() else new_char)
            
        return "".join(result)
    
    def decrypt(self, text: str, shift: str, alphabet: Alphabet) -> str:
        result = []
        alphabet_length = len(alphabet.value)
        
        for char in text:
            char_index = alphabet.value.find(char.lower())
            
            if char_index == -1: # When find() doesn't find the char, appends the exact char 
                result.append(char)
                continue
            
            new_char = alphabet.value[(char_index - int(shift)) % alphabet_length]
            # Preserve uppercase if the original character was uppercase
            result.append(new_char.upper() if char.isupper() else new_char)
            
        return "".join(result)
    
    
if __name__ == "__main__":
    cipher = CesarCipher()
    
    action_in = int(input("What do you want to do? \n 1) Encrypt\n 2) Decrypt\n: "))
    text_in = input("Insert the text: ")
    shift_in = input("How many shifts do you want? ")
    alphabet_in = int(input("Which alphabet do you want? \n 1) English\n 2) Spanish\n: "))
    
    match alphabet_in:
        case 1:
            selected_alphabet = Alphabet.ENGLISH
        case 2:
            selected_alphabet = Alphabet.SPANISH
        case _:
            print("Invalid option. Using the English alphabet by default.")
            selected_alphabet = Alphabet.ENGLISH
        
    match action_in:
        case 1:
            result = cipher.encrypt(text_in, shift_in, selected_alphabet)
            print("Encrypted text: " + result)
        case 2:
            result = cipher.decrypt(text_in, shift_in, selected_alphabet)
            print("Decrypted text: " + result)
        case _:
            print("Invalid option. Encrypting by default.")
            result = cipher.encrypt(text_in, shift_in, selected_alphabet)
            print("Encrypted text: " + result)