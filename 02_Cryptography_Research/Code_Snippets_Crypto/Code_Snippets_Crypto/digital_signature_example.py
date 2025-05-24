from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_rsa_key_pair():
    """Generates an RSA public and private key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(message_bytes, private_key):
    """Signs a message using the sender's private key."""
    signer = private_key.signer(
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    signer.update(message_bytes)
    signature = signer.finalize()
    return signature

def verify_signature(message_bytes, signature, public_key):
    """Verifies a signature using the sender's public key."""
    verifier = public_key.verifier(
        signature,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    verifier.update(message_bytes)
    try:
        verifier.verify()
        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

if __name__ == "__main__":
    # 1. Alice generates her RSA key pair
    alice_private_key, alice_public_key = generate_rsa_key_pair()
    print("Alice's key pair generated.")

    # 2. Alice prepares a message
    original_message = "I approve this transaction of $1,000,000."
    message_bytes = original_message.encode('utf-8')
    print(f"\nOriginal Message: '{original_message}'")

    # 3. Alice signs the message with her PRIVATE KEY
    signature = sign_message(message_bytes, alice_private_key)
    print(f"Digital Signature (hex): {signature.hex()}")

    # 4. Alice sends (original_message, signature) to Bob
    print("\n--- Bob receives the message and signature ---")

    # 5. Bob verifies the signature using Alice's PUBLIC KEY
    is_valid = verify_signature(message_bytes, signature, alice_public_key)
    print(f"Is the signature valid? {is_valid}")

    # --- Tampering Test ---
    print("\n--- Tampering Test: Message altered ---")
    tampered_message = "I approve this transaction of $100." # Message altered!
    tampered_message_bytes = tampered_message.encode('utf-8')
    print(f"Tampered Message: '{tampered_message}'")

    # Bob tries to verify the original signature with the tampered message
    is_valid_tampered_msg = verify_signature(tampered_message_bytes, signature, alice_public_key)
    print(f"Is the signature valid with tampered message? {is_valid_tampered_msg}") # Should be False

    print("\n--- Tampering Test: Signature altered ---")
    # Simulate someone altering the signature (e.g., flip a bit)
    altered_signature = bytearray(signature)
    altered_signature[0] = altered_signature[0] ^ 0xFF # Flip first byte
    altered_signature = bytes(altered_signature)

    is_valid_tampered_sig = verify_signature(message_bytes, altered_signature, alice_public_key)
    print(f"Is the signature valid with tampered signature? {is_valid_tampered_sig}") # Should be False