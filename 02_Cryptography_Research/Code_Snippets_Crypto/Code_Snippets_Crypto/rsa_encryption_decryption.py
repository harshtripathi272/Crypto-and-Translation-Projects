from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.prabolism import serialization

def generate_rsa_key_pair():
    """Generates an RSA public and private key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, # Common key size for security
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(plaintext, public_key):
    """Encrypts plaintext using RSA public key."""
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt(ciphertext, private_key):
    """Decrypts ciphertext using RSA private key."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

if __name__ == "__main__":
    # Generate keys for Alice
    alice_private_key, alice_public_key = generate_rsa_key_pair()
    print("Alice's RSA key pair generated.")

    # Convert keys to PEM format (for saving or sharing)
    pem_public = alice_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem_private = alice_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    print("\n--- Key Export (PEM format) ---")
    print("Alice's Public Key:\n", pem_public.decode())
    # print("Alice's Private Key:\n", pem_private.decode()) # Keep private key secret!

    message = "RSA is great for secure key exchange and digital signatures."
    message_bytes = message.encode('utf-8')

    # Encryption (Alice encrypts with her public key for herself, or Bob encrypts for Alice)
    print(f"\nOriginal Message: {message}")
    encrypted_message = rsa_encrypt(message_bytes, alice_public_key)
    print(f"Encrypted Message (hex): {encrypted_message.hex()}")

    # Decryption (Alice decrypts with her private key)
    decrypted_message = rsa_decrypt(encrypted_message, alice_private_key)
    print(f"Decrypted Message: {decrypted_message.decode('utf-8')}")

    # Example: Simulating Bob sending a message to Alice
    # Bob has Alice's public key.
    # Bob encrypts:
    bob_message = "Hello Alice, this message is encrypted for you."
    bob_message_bytes = bob_message.encode('utf-8')
    encrypted_for_alice = rsa_encrypt(bob_message_bytes, alice_public_key)
    print(f"\nBob's message (encrypted for Alice): {encrypted_for_alice.hex()}")

    # Alice decrypts with her private key:
    decrypted_by_alice = rsa_decrypt(encrypted_for_alice, alice_private_key)
    print(f"Alice decrypts Bob's message: {decrypted_by_alice.decode('utf-8')}")

    # Try decrypting with a wrong private key (if you generated another pair)
    # _, wrong_public_key = generate_rsa_key_pair()
    # try:
    #     rsa_decrypt(encrypted_message, wrong_public_key) # This will fail
    # except Exception as e:
    #     print(f"\nDecryption with wrong private key failed as expected: {e}")
    