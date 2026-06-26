import re
import random

from database import get_all_movie_codes

def generate_movie_code():
    used_code = get_all_movie_codes()
    
    while True:
        code = random.randint(1, 999)

        if code not in used_code:
            return code
        



def get_movie_name(description):
    match = re.search(r"🍿 \| Nomi:\s*(.+)", description)

    if match:
        return match.group(1).strip()

    return "Noma'lum"