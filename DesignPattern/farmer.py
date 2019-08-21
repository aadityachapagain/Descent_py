from .plant import generate_info
import random
from string import ascii_letters


def generate_random_data():
    args = ['clean', 'default']
    info = {}
    for _ in range(random.randint(1,3)):
        val = ''.join(random.choices(ascii_letters,k=20))
        info.update({random.randint(2000, 3000):val})
    
    generate_info(random.choice(args), info)