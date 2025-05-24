from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def aes_encrypt(plaintext, key):
    """Encrypts plaintext using AES in CBC mode with a random IV."""
    # Generate a random 16-byte IV
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return iv, ciphertext # Return IV along with ciphertext

def aes_decrypt(ciphertext, key, iv):
    """Decrypts ciphertext using AES in CBC mode with the given key and IV."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_text = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted text
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(decrypted_padded_text) + unpadder.finalize()
    return plaintext

if __name__ == "__main__":
    # Generate a random 256-bit (32-byte) AES key
    aes_key = os.urandom(32) # AES-256
    print(f"Generated AES Key (hex): {aes_key.hex()}")

    message = "This is a secret message that needs to be kept confidential."
    message_bytes = message.encode('utf-8')

    # Encrypt
    iv, encrypted_message = aes_encrypt(message_bytes, aes_key)
    print(f"\nOriginal Message: {message}")
    print(f"Encrypted Message (hex): {encrypted_message.hex()}")
    print(f"Initialization Vector (IV) (hex): {iv.hex()}")

    # Decrypt
    decrypted_message = aes_decrypt(encrypted_message, aes_key, iv)
    print(f"Decrypted Message: {decrypted_message.decode('utf-8')}")

    # Test with incorrect key (should fail or decrypt to gibberish)
    print("\n--- Testing with incorrect key ---")
    incorrect_key = os.urandom(32)
    try:
        decrypted_wrong_key = aes_decrypt(encrypted_message, incorrect_key, iv)
        print(f"Decrypted with wrong key: {decrypted_wrong_key.decode('utf-8')}")
    except Exception as e:
        print(f"Decryption with wrong key failed as expected: {e}")

    # Test with incorrect IV (should fail or decrypt to gibberish)
    print("\n--- Testing with incorrect IV ---")
    incorrect_iv = os.urandom(16)
    try:
        decrypted_wrong_iv = aes_decrypt(encrypted_message, aes_key, incorrect_iv)
        print(f"Decrypted with wrong IV: {decrypted_wrong_iv.decode('utf-8')}")
    except Exception as e:
        print(f"Decryption with wrong IV failed as expected: {e}")