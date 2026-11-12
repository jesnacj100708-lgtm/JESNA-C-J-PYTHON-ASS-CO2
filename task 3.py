import re, timeit
def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    return text.strip().replace(" ", "").replace("-", "").upper()
def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    if len(reg) != 9 and len(reg) != 10:
        return False
    return (reg[:2].isalpha() and reg[2:4].isdigit()
            and reg[4:-4].isalpha() and reg[-4:].isdigit())
def format_plate(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' (only for valid numbers)."""
    return reg[:2] + " " + reg[2:4] + " " + reg[4:-4] + " " + reg[-4:]
def is_valid_regex(reg):
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None
if __name__ == "__main__":
    print("--- Complete the Code ---")
    for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")
    print("\n--- Six designed inputs: prediction vs observed ---")
    tests = [("tn 09 ab 1234", True), ("TN-09-AB-1234", True), ("Tn09Ab1234", True),
             ("ka-01-m-0007", True), ("TN09ABC1234", False), ("TN 09 AB 123", False)]
    for raw, expected in tests:
        reg = normalise(raw); ok = is_valid(reg)
        out = format_plate(reg) if ok else "-"
        print(f"{raw:15} pred={str(expected):5} obs={str(ok):5} {'PASS' if ok == expected else 'FAIL'}  receipt: {out}")
    print("\n--- Immutability and slicing ---")
    text = "tn09ab1234"
    print("text.upper() ->", text.upper(), "| text is still ->", text)
    try:
        text[0] = "T"
    except TypeError as e:
        print("text[0] = 'T' ->", "TypeError:", e)
    for s in ("KA01M0007", "TN09AB1234"):
        print(f"{s} (len {len(s)}): s[-4:] = {s[-4:]!r}  s[4:-4] = {s[4:-4]!r}")
    print("\n--- Slicing vs regular expression ---")
    pool = ["TN09AB1234", "KA01M0007", "TN9AB1234", "TN221234AB", "TN09ABC1234", "", "T"] * 1000
    assert all(is_valid(p) == is_valid_regex(p) for p in pool)
    print("both validators agree on", len(pool), "inputs")
    N = 200_000
    t1 = timeit.timeit(lambda: is_valid("TN09AB1234"), number=N)
    t2 = timeit.timeit(lambda: is_valid_regex("TN09AB1234"), number=N)
    print(f"slicing: {t1/N*1e9:.0f} ns/call   regex: {t2/N*1e9:.0f} ns/call")
