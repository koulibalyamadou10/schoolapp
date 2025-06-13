import random
import string

def generate_random_password(length=16):
    # Caractères obligatoires
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()-_=+[]{};:,.<>?")

    # Compléter avec des caractères aléatoires
    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
    remaining = [random.choice(all_chars) for _ in range(remaining_length)]

    # Mélanger tous les caractères
    password_list = list(lowercase + uppercase + digit + special) + remaining
    random.shuffle(password_list)
    return ''.join(password_list)