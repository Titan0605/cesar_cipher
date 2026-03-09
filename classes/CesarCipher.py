from enums import Alphabet

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