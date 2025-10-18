import math
import re

def charspace_score(pw: str) -> int:
    s = 0
    s += 26 if re.search(r"[a-z]", pw) else 0
    s += 26 if re.search(r"[A-Z]", pw) else 0
    s += 10 if re.search(r"[0-9]", pw) else 0
    s += 32 if re.search(r"[^A-Za-z0-9]", pw) else 0
    return max(s, 1)

def estimate_entropy_bits(pw: str) -> float:
    # naive estimate: len * log2(charspace)
    return len(pw) * math.log2(charspace_score(pw))
