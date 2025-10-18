import argparse
from pathlib import Path
from tabulate import tabulate
from .checker import check_password, load_breached_list

def main():
    ap = argparse.ArgumentParser(description="Local password strength + leak checker (privacy-first).")
    ap.add_argument("-p", "--password", help="Password to evaluate (or leave blank to prompt)", default=None)
    ap.add_argument("-f", "--file", help="Path to local breached-password subset", default="data/common_passwords.txt")
    args = ap.parse_args()

    if args.password is None:
        import getpass
        pw = getpass.getpass("Enter password (hidden): ")
    else:
        pw = args.password

    breached = load_breached_list(Path(args.file))
    result = check_password(pw, breached)

    rows = [
        ["Entropy (bits)", result["entropy_bits"]],
        ["Grade", result["grade"]],
        ["Found in local breach list", "YES" if result["leaked_locally"] else "NO"],
        ["Issues", "\n".join(result["issues"]) if result["issues"] else "None"],
    ]
    print(tabulate(rows, headers=["Metric", "Value"], tablefmt="github"))

if __name__ == "__main__":
    main()
