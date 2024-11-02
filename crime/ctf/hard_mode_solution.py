# exploit.py
# Skeleton for building your CRIME attack
from requester import *
import random

class CrimeSolver:
    def __init__(self, url, difficulty):
        self.oracle = CRIMERequester(url)
        self.difficulty = difficulty

    def find_flag(self, known):
        # CRIME Attack Challenge.
        """
        TODO: Implement your attack here!

        Tips for building your exploit:
        1. We know the flag format is CTF_FLAG{...}
        2. The server response contains 'secret_flag: <THE_FLAG>'
        3. Compression works better when strings match
        """
        charset = string.ascii_letters + string.digits + "{}_}"  # Possible flag characters

        for char in charset:
            request1 =  "".join(known) + char + "~#/[|/ç" 
            request2 =  "".join(known) + "~#/[|/ç" + char
            len1 = self.oracle.get_response_length(request1.encode(), self.difficulty)
            len2 = self.oracle.get_response_length(request2.encode(), self.difficulty)
            if len1 < len2:
                t = list(known)
                t.append(char)
                t_text = "".join(t)
                print(f"\n\r possible_flag_prefix = {t_text}")
                self.find_flag(t)
    

    def adjust_padding(self, known):
        garb = ''
        l = 0
        original_length = self.oracle.get_response_length(garb + "".join(known) , self.difficulty)
        while True:  
            enc_len = self.oracle.get_response_length(garb +"".join(known), self.difficulty)
            if enc_len > original_length:
                break
            else:
                l += 1
                garb = ''.join(random.sample(string.ascii_lowercase + string.digits, k=l))
        return garb[:-1]
        


def main():
    url = "http://localhost:8443"  # Update this to the actual server URL
    known = "secret_flag: CTF_FLAG{"

    difficulty = None
    # difficulty = DifficultyLevel.NORMAL
    difficulty = DifficultyLevel.HARD
    assert (
        difficulty
    ), "Please choose a difficulty level, Normal: (Compression). Hard: (Compression + Encryption)."
    solver = CrimeSolver(url,difficulty)

    print(f"Starting attack in {difficulty.name} mode...")
    print(f"Known prefix: {known}")

    for i in range(30):
        print ("0000000000000000000000000000000000000000000")
        garb = solver.adjust_padding(known)
        flag = solver.find_flag(garb + "\n" + known)

if __name__ == "__main__":
    main()
