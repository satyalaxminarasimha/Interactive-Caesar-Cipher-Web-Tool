import re

def check_password_strength(password):
    """Evaluates password strength and provides feedback."""
    strength = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        strength += 1
    else:
        feedback.append("Password should include both uppercase and lowercase letters.")

    # Numbers Check
    if re.search(r'[0-9]', password):
        strength += 1
    else:
        feedback.append("Password should include at least one number.")

    # Special Characters Check
    if re.search(r'[!@#$%^&*()_\-+=<>?/]', password):
        strength += 1
    else:
        feedback.append("Password should include at least one special character.")

    # Strength Levels
    strength_levels = {1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    password_strength = strength_levels.get(strength, "Very Weak")

    print(f"Password Strength: {password_strength}")
    if feedback:
        print("Suggestions:")
        for tip in feedback:
            print(f"- {tip}")

# Example Usage
user_password = input("Enter a password to check its strength: ")
check_password_strength(user_password)