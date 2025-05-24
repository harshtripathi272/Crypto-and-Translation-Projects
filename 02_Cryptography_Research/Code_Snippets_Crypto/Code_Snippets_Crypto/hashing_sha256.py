import hashlib

def generate_sha256_hash(data):
    """Generates the SHA-256 hash of the given data."""
    if isinstance(data, str):
        data = data.encode('utf-8') # Encode string to bytes
    elif not isinstance(data, bytes):
        raise TypeError("Input must be string or bytes.")

    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

if __name__ == "__main__":
    message1 = "The quick brown fox jumps over the lazy dog."
    message2 = "The quick brown fox jumps over the lazy cat."
    message3 = "The quick brown fox jumps over the lazy dog." # Same as message1

    print(f"Message 1: '{message1}'")
    hash1 = generate_sha256_hash(message1)
    print(f"SHA-256 Hash 1: {hash1}")

    print(f"\nMessage 2: '{message2}'")
    hash2 = generate_sha256_hash(message2)
    print(f"SHA-256 Hash 2: {hash2}")

    print(f"\nMessage 3: '{message3}' (Same as Message 1)")
    hash3 = generate_sha256_hash(message3)
    print(f"SHA-256 Hash 3: {hash3}")

    print("\n--- Hash Comparison ---")
    print(f"Hash 1 == Hash 3: {hash1 == hash3} (Identical inputs produce identical hashes)")
    print(f"Hash 1 == Hash 2: {hash1 == hash2} (Different inputs produce different hashes)")

    # Example: Verifying file integrity
    file_content = b"This is the content of my important file."
    original_hash = generate_sha256_hash(file_content)
    print(f"\nOriginal file content hash: {original_hash}")

    # Simulate accidental modification
    modified_content = b"This is the content of my important file! (modified)"
    modified_hash = generate_sha256_hash(modified_content)
    print(f"Modified file content hash: {modified_hash}")

    print(f"Hashes match (integrity check): {original_hash == modified_hash}")

    # Example: Password storage (simplified)
    user_password = "MySuperSecretPassword123"
    stored_hash = generate_sha256_hash(user_password)
    print(f"\nSimulated stored password hash: {stored_hash}")

    # User attempts to log in
    login_attempt_password = "MySuperSecretPassword123"
    login_attempt_hash = generate_sha256_hash(login_attempt_password)

    print(f"Login attempt hash matches stored hash: {login_attempt_hash == stored_hash}")

    # Incorrect login attempt
    wrong_password = "MyWrongPassword"
    wrong_password_hash = generate_sha256_hash(wrong_password)
    print(f"Incorrect login attempt hash matches stored hash: {wrong_password_hash == stored_hash}")