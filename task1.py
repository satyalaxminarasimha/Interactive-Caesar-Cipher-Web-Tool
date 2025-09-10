def caesar_cipher(text, shift, mode="encrypt"):
    result = ""
    if mode == "decrypt":
        shift = -shift  
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(char.lower()) - ord('a') + shift_amount) % 26) + ord('a'))
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result
mode = input("Enter 'encrypt' to encrypt or 'decrypt' to decrypt:").strip().lower()
message = input("Enter your message: ")
shift_value = int(input("Enter the shift value:"))
output = caesar_cipher(message, shift_value, mode)
print(f"Result: {output}")