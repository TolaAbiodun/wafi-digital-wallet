import random

def generate_account_no():
    'Generates a 10 digit account no for a user'
    fixed_digits = 10 
    return random.randrange(1111111111, 9999999999, fixed_digits)
