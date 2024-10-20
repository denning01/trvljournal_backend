from werkzeug.security import generate_password_hash

# Define the password you want to hash
password = 'password1'
hashed_password = generate_password_hash(password)

print(f"Hashed password for '{password}': {hashed_password}")

