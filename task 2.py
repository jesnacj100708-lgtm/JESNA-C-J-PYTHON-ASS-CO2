CORRECT = "4821"
def make_reader(values):
    it = iter(values)
    return lambda: next(it)
def otp_while(read, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        entry = read().strip()
        if entry == "":
            print("  (blank entry - not counted)")
            continue                      # skip the counter update
        attempts += 1                     # counter updated AFTER the blank check
        if entry == CORRECT:
            print("  OTP verified")
            break                         # success: leave loop, skip else
        else:
            pass                          # placeholder: audit-log hook to be added
        print(f"  wrong OTP ({attempts}/{max_attempts})")
    else:                                 # runs only if loop ended without break
        print("  ACCOUNT LOCKED for 30 minutes")
        return "locked"
    return "verified"
def otp_for(read):
    for attempt in range(1, 4):
        while True:                       # re-prompt on blank without using an attempt
            entry = read().strip()
            if entry != "":
                break
            print("  (blank entry - not counted)")
        if entry == CORRECT:
            print("  OTP verified")
            break
        else:
            pass
        print(f"  wrong OTP ({attempt}/3)")
    else:
        print("  ACCOUNT LOCKED for 30 minutes")
        return "locked"
    return "verified"
def otp_for_continue_bug(read):
    for attempt in range(1, 4):
        entry = read().strip()
        if entry == "":
            print("  (blank) - but range(3) already used up this attempt!")
            continue
        if entry == CORRECT:
            print("  OTP verified"); break
        print(f"  wrong OTP ({attempt}/3)")
    else:
        print("  ACCOUNT LOCKED for 30 minutes"); return "locked"
    return "verified"
def otp_while_counter_bug(read, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1                     # BUG: counter updated before the blank check
        entry = read().strip()
        if entry == "":
            print("  (blank entry) counted as attempt", attempts)
            continue
        if entry == CORRECT:
            print("  OTP verified"); break
        print(f"  wrong OTP ({attempts}/{max_attempts})")
    else:
        print("  ACCOUNT LOCKED for 30 minutes"); return "locked"
    return "verified"
def otp_extended(read, security_ok):
    allowed, extra_given, attempts = 3, False, 0
    while attempts < allowed:
        entry = read().strip()
        if entry == "":
            print("  (blank entry - not counted)"); continue
        attempts += 1
        if entry == CORRECT:
            print("  OTP verified"); break
        print(f"  wrong OTP ({attempts}/{allowed})")
        if attempts == allowed and not extra_given:
            print("  security question asked ->", "correct" if security_ok else "wrong")
            if security_ok:
                allowed += 2; extra_given = True
                print("  two extra attempts granted, allowed =", allowed)
    else:
        print("  ACCOUNT LOCKED for 30 minutes"); return "locked"
    return "verified"
def otp_recursive(read, attempt=1, max_attempts=3):
    entry = read().strip()
    if entry == "":
        return otp_recursive(read, attempt, max_attempts)
    if entry == CORRECT:
        return "verified"
    if attempt == max_attempts:
        return "locked"
    return otp_recursive(read, attempt + 1, max_attempts)
if __name__ == "__main__":
    demo = ["", "1111", "", "2222", "3333", "4821"]
    print("1. while version  (blank, wrong, blank, wrong, wrong):"); print(" result:", otp_while(make_reader(demo)))
    print("2. for version    (same input):"); print(" result:", otp_for(make_reader(demo)))
    print("3. success on 2nd try (1111, 4821):"); print(" result:", otp_while(make_reader(["1111", "4821"])))
    print("4. for + continue bug (blank, 1111, 2222, 4821):"); print(" result:", otp_for_continue_bug(make_reader(["", "1111", "2222", "4821"])))
    print("5. counter-in-wrong-place bug (blank, blank, 0000, 4821):"); print(" result:", otp_while_counter_bug(make_reader(["", "", "0000", "4821"])))
    print("6. changed condition, security answer correct (3 wrong, then 9999, 4821):")
    print(" result:", otp_extended(make_reader(["1", "2", "3", "9999", "4821"]), True))
    print("7. changed condition, security answer wrong:")
    print(" result:", otp_extended(make_reader(["1", "2", "3", "4821"]), False))
    print("8. recursive version:", otp_recursive(make_reader(["", "1111", "2222", "3333"])),
          "|", otp_recursive(make_reader(["1111", "4821"])))
    blanks = [""] * 5000 + [CORRECT]
    try:
        print("9. recursion, 5000 blank entries:", otp_recursive(make_reader(blanks)))
    except RecursionError as e:
        print("9. recursion, 5000 blank entries: RecursionError ->", e)
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        r = otp_while(make_reader(blanks))
    print("   while loop, same 5000 blanks:", r)
