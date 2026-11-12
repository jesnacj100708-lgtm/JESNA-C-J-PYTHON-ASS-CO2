import timeit
# household = (units, has_ration_card, has_member_above_80)
HOUSEHOLDS = [
    (50, True, False), (100, True, False), (101, True, False), (101, False, False),
    (200, True, False), (200, False, False), (201, False, True), (201, False, False),
]
def subsidy_buggy(units, card, elder):
    """Separate if statements - every condition is tested independently."""
    result = []
    if units <= 100:
        result.append("FULL")
    if units <= 200 and card:            # no lower bound -> overlaps with rule 1
        result.append("PARTIAL")
    if units > 200 and elder:
        result.append("SENIOR")
    return result or ["NONE"]
def subsidy(units, card, elder):
    """if-elif-else - exactly one branch runs."""
    if units <= 100:
        return "FULL"
    elif 101 <= units <= 200 and card:
        return "PARTIAL"
    elif units > 200 and elder:
        return "SENIOR"
    else:
        return "NONE"
def subsidy_nested(units, card, elder):
    """Nested-if version used only for the design comparison."""
    if units <= 100:
        return "FULL"
    else:
        if units <= 200:
            if card:
                return "PARTIAL"
            else:
                return "NONE"
        else:
            if elder:
                return "SENIOR"
            else:
                return "NONE"
def subsidy_match(units, card, elder):
    match units:
        case u if u <= 100:
            return "FULL"
        case u if u <= 200 and card:
            return "PARTIAL"
        case u if u > 200 and elder:
            return "SENIOR"
        case _:
            return "NONE"
def make_slabs(k):
    """k-1 ordinary slabs followed by the final open slab (worst case = last slab)."""
    slabs = [(100 + i, "FULL", None) for i in range(k - 1)]
    slabs.append((float("inf"), "SENIOR", "elder"))
    return slabs
def subsidy_table(units, card, elder, slabs):
    flags = {"card": card, "elder": elder}
    for upper, label, need in slabs:
        if units <= upper:
            return label if (need is None or flags[need]) else "NONE"
    return "NONE"
if __name__ == "__main__":
    print(f"{'units':>5} {'card':>5} {'80+':>5} | {'separate if':<16} | if-elif-else")
    for u, c, e in HOUSEHOLDS:
        b = "+".join(subsidy_buggy(u, c, e)); g = subsidy(u, c, e)
        flag = "  <-- TWO subsidies" if "+" in b else ""
        print(f"{u:>5} {str(c):>5} {str(e):>5} | {b:<16} | {g}{flag}")
    # exhaustive check 0..400 units x card x elder
    dup = 0; same = 0; total = 0
    for u in range(0, 401):
        for c in (True, False):
            for e in (True, False):
                total += 1
                if len(subsidy_buggy(u, c, e)) > 1: dup += 1
                r = subsidy(u, c, e)
                assert r == subsidy_nested(u, c, e) == subsidy_match(u, c, e)
                assert r == subsidy_table(u, c, e, make_slabs(3)[:0] or [(100,"FULL",None),(200,"PARTIAL","card"),(float("inf"),"SENIOR","elder")])
                same += 1
    print(f"\nExhaustive check: {total} cases, buggy gave 2+ subsidies in {dup}; "
          f"elif / nested / match / table agree in {same}/{total}")
    print("\nTime per decision (worst case, 200,000 calls):")
    N = 200_000
    t = timeit.timeit(lambda: subsidy(250, False, True), number=N); print(f"  if-elif-else          {t/N*1e9:8.1f} ns")
    t = timeit.timeit(lambda: subsidy_match(250, False, True), number=N); print(f"  match-case            {t/N*1e9:8.1f} ns")
    for k in (3, 30, 300):
        s = make_slabs(k)
        t = timeit.timeit(lambda: subsidy_table(250, False, True, s), number=N)
        print(f"  slab table, k={k:<4}     {t/N*1e9:8.1f} ns")
