from PIL import Image
import numpy as np

def encrypt_image(input_path, output_path, key):
    """Encrypt an image by modifying pixel values."""
    img = Image.open(input_path)
    img_array = np.array(img, dtype=np.uint8)  # Ensure array type is uint8
    
    # Encrypt by shifting pixel values while preventing overflow
    encrypted_array = np.clip(img_array + key, 0, 255)  
    
    encrypted_img = Image.fromarray(encrypted_array.astype(np.uint8))
    encrypted_img.save(output_path)
    print(f"Image encrypted and saved as {output_path}")

def decrypt_image(input_path, output_path, key):
    """Decrypt an image by reversing pixel modifications."""
    img = Image.open(input_path)
    img_array = np.array(img, dtype=np.uint8)
    
    # Decrypt by reversing the transformation while preventing underflow
    decrypted_array = np.clip(img_array - key, 0, 255)  
    
    decrypted_img = Image.fromarray(decrypted_array.astype(np.uint8))
    decrypted_img.save(output_path)
    print(f"Image decrypted and saved as {output_path}")

# User input handling
operation = input("Enter 'encrypt' or 'decrypt': ").strip().lower()
input_file = input("Enter input image path: ").strip()
output_file = input("Enter output image path: ").strip()
key = int(input("Enter encryption key (integer): "))

if operation == "encrypt":
    encrypt_image(input_file, output_file, key)
elif operation == "decrypt":
    decrypt_image(input_file, output_file, key)
else:
    print("Invalid operation selected. Please enter 'encrypt' or 'decrypt'.")