import hashlib
import re
from pathlib import Path
from .entropy import estimate_entropy_bits

WEAK_PATTERNS = [
    r"(password|admin|welcome|letmein)",
    r"(qwerty|asdf|zxcv)",
    r"(\d{4,})"  # long digit runs, e.g., 123456
]

def load_breached_list(path: Path) -> set:
    # file contains plain passwords, one per line (small subset for demo)
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()}

def strength_grade(entropy_bits: float) -> str:
    if entropy_bits < 35: return "Very Weak"
    if entropy_bits < 50: return "Weak"
    if entropy_bits < 65: return "Moderate"
    if entropy_bits < 80: return "Strong"
    return "Very Strong"

def check_password(pw: str, breached: set) -> dict:
    issues = []

    # basic rules
    if len(pw) < 12:
        issues.append("Use at least 12 characters.")
    if not re.search(r"[A-Z]", pw): issues.append("Add uppercase letters.")
    if not re.search(r"[a-z]", pw): issues.append("Add lowercase letters.")
    if not re.search(r"[0-9]", pw): issues.append("Add digits.")
    if not re.search(r"[^A-Za-z0-9]", pw): issues.append("Add symbols.")

    # weak patterns
    for pat in WEAK_PATTERNS:
        if re.search(pat, pw.lower()):
            issues.append("Avoid common words or simple sequences.")

    # breached check (local list only)
    leaked = (pw in breached)

    # entropy & grade
    entropy = round(estimate_entropy_bits(pw), 1)
    grade = strength_grade(entropy)

    return {
        "entropy_bits": entropy,
        "grade": grade,
        "leaked_locally": leaked,
        "issues": issues
    }
