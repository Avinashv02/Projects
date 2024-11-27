import bcrypt

def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

passwords = ["password123"]  # Replace with your actual plaintext passwords
hashed_passwords = [hash_password(password) for password in passwords]

print("Hashed Passwords:", hashed_passwords)
