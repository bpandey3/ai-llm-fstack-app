# Symmetric encryption example (A to B and B to A) using cryptography

!pip install cryptography

from cryptography.fernet import Fernet

# Generate a key (keep this secret!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Original message
original_message = b"My top secret message"

# Encrypt (A → B)
encrypted = cipher.encrypt(original_message)

# Decrypt (B → A)
decrypted = cipher.decrypt(encrypted)

# Display results
print("Encryption Key:", key.decode())
print("Original Message:", original_message)
print("Encrypted Message:", encrypted.decode())
print("Decrypted Message:", decrypted.decode())
