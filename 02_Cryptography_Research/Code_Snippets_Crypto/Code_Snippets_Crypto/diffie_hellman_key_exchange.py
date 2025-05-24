from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import os

def generate_dh_parameters():
    """Generates Diffie-Hellman parameters (p, g)."""
    # For demonstration, using a smaller key size.
    # For real applications, use at least 2048 or 3072 bits.
    parameters = dh.generate_parameters(generator=2, key_size=1024, backend=default_backend())
    return parameters

def perform_dh_key_exchange():
    """Simulates Diffie-Hellman key exchange between Alice and Bob."""
    print("--- Diffie-Hellman Key Exchange ---")

    # 1. Agree on Public Parameters (p, g)
    parameters = generate_dh_parameters()
    print("Public DH parameters (p, g) generated.")

    # 2. Alice generates her private key and public key
    alice_private_key = parameters.generate_private_key(backend=default_backend())
    alice_public_key = alice_private_key.public_key()
    print("Alice generated her private and public keys.")

    # 3. Bob generates his private key and public key
    bob_private_key = parameters.generate_private_key(backend=default_backend())
    bob_public_key = bob_private_key.public_key()
    print("Bob generated his private and public keys.")

    # 4. Exchange Public Keys (over insecure channel)
    # Alice sends alice_public_key to Bob
    # Bob sends bob_public_key to Alice
    print("\nPublic keys exchanged.")

    # 5. Alice computes shared secret using Bob's public key and her private key
    alice_shared_key = alice_private_key.exchange(bob_public_key)
    print("Alice computed shared key.")

    # 6. Bob computes shared secret using Alice's public key and his private key
    bob_shared_key = bob_private_key.exchange(alice_public_key)
    print("Bob computed shared key.")

    # Derive a fixed-length key from the shared secret (e.g., for AES)
    # Using HKDF (HMAC-based Key Derivation Function) for best practice
    derived_key_length = 32 # For AES-256

    alice_derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=derived_key_length,
        salt=None,
        info=b'handshake data', # Contextual information
        backend=default_backend()
    ).derive(alice_shared_key)

    bob_derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=derived_key_length,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    ).derive(bob_shared_key)

    print("\n--- Verification ---")
    print(f"Alice's derived key (hex): {alice_derived_key.hex()}")
    print(f"Bob's derived key (hex):   {bob_derived_key.hex()}")

    if alice_derived_key == bob_derived_key:
        print("\n✅ Shared secret key successfully established!")
        print("This derived key can now be used for symmetric encryption (e.g., AES) for secure communication.")
    else:
        print("\n❌ Shared secret key mismatch! Something went wrong.")

if __name__ == "__main__":
    perform_dh_key_exchange()
    