import sys, time
# ---------- ORIGINAL (diagnosed in Q6) ----------
calls = 0
def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)
# ---------- REDESIGN: bottom-up, keep only the last two values ----------
adds = 0
def ways_fast(n):
    global adds
    prev, cur = 1, 1                 # ways(0), ways(1)
    for _ in range(n - 1):           # each ways(k) is computed exactly once
        prev, cur = cur, prev + cur
        adds += 1
    return cur
# ---------- Redesign variant with explicit dictionary (top-down) ----------
def ways_dict(n, memo=None):
    global calls
    if memo is None:
        memo = {}
    calls += 1
    if n <= 1:
        return 1
    if n not in memo:
        memo[n] = ways_dict(n - 1, memo) + ways_dict(n - 2, memo)
    return memo[n]
def best_time(fn, n, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        s = time.perf_counter(); fn(n); best = min(best, time.perf_counter() - s)
    return best
if __name__ == "__main__":
    print("A. Evidence of repeated work in the original (counts of calls per argument, n = 10)")
    from collections import Counter
    seen = Counter()
    def traced(n):
        seen[n] += 1
        return 1 if n <= 1 else traced(n - 1) + traced(n - 2)
    traced(10)
    print("   calls for argument 1:", seen[1], "| argument 2:", seen[2], "| argument 5:", seen[5], "| argument 10:", seen[10])
    print("   distinct arguments:", len(seen), "| total calls:", sum(seen.values()), "-> repeated calls:", sum(seen.values()) - len(seen))
    print("\nE. Original vs redesign, same inputs")
    print(f"{'n':>3} | {'naive calls':>12} {'naive time(s)':>14} | {'fast adds':>9} {'fast time(s)':>13} | {'dict calls':>10} | {'speed-up':>10}")
    for n in (10, 20, 25, 30, 32):
        calls = 0; r1 = ways_naive(n); cn = calls
        tn = best_time(ways_naive, n)
        adds = 0; r2 = ways_fast(n); ad = adds
        tf = best_time(ways_fast, n)
        calls = 0; r3 = ways_dict(n); cd = calls
        assert r1 == r2 == r3
        print(f"{n:>3} | {cn:>12} {tn:>14.6f} | {ad:>9} {tf:>13.8f} | {cd:>10} | {tn/tf:>9.0f}x")
    print("\nSame answers for n = 1..30:", all(ways_fast(n) == ways_dict(n) for n in range(1, 31)))
    print("\nLarge inputs (original impossible):")
    for n in (1000, 10000, 100000):
        t = best_time(ways_fast, n)
        print(f"   n = {n:>6}: fast version {t:.6f} s, recursion depth used = 1")
    print("   dict version at n = 1000 with default limit:", end=" ")
    try:
        ways_dict(1000); print("ok")
    except RecursionError:
        print("RecursionError")
