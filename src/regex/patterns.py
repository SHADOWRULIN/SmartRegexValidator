import re

def validate_email(email: str) -> bool:
    """
    Validates an email address based on standard rules:
    - Must have a username
    - Must contain an '@' symbol
    - Must contain a domain
    - Must contain a dot and an extension
    """
    # Pattern explanation: 
    # ^ starts string, [a-zA-Z0-9_.-]+ matches username, @ matches symbol
    # [a-zA-Z0-9-]+ matches domain, \. matches dot, [a-zA-Z0-9-.]+$ matches extension at end
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(email_pattern, email):
        return True
    return False

def validate_password(password: str) -> bool:
    """
    Validates a password based on strict rules:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 digit
    """
    # Pattern explanation using lookaheads (?=...):
    # (?=.*[a-z]) ensures 1 lowercase, (?=.*[A-Z]) ensures 1 uppercase
    # (?=.*\d) ensures 1 digit, .{8,} ensures at least 8 characters long
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    
    if re.match(password_pattern, password):
        return True
    return False

# --- TESTING BLOCK ---
# This code only runs if you execute this file directly. 
# It will not run when imported by the main GUI later.
if __name__ == "__main__":
    print("--- Email Testing ---")
    test_emails = ["abc@gmail.com", "john123@yahoo.com", "invalid-email", "missing@domain"]
    for e in test_emails:
        status = "Valid" if validate_email(e) else "Invalid"
        print(f"[{status}] {e}")

    print("\n--- Password Testing ---")
    test_passwords = ["Abc12345", "weakpass", "Nolowercase123!", "Short1!"]
    for p in test_passwords:
        status = "Valid" if validate_password(p) else "Invalid"
        print(f"[{status}] {p}")