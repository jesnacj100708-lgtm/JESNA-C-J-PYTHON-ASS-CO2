import sys, time
from functools import lru_cache
calls = 0
def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)
@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)
def ways_loop(n):
    a, b = 1, 1                      # ways(0), ways(1)
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1
if __name__ == "__main__":
    print("--- Complete the Code ---")
    calls = 0; print("naive:", ways_naive(25), "calls", calls)
    calls = 0; print("memo:", ways_memo(25), "calls", calls)
    print("\n--- Correctness n = 1..6 (hand: 1, 2, 3, 5, 8, 13) ---")
    print([ways_naive(n) for n in range(1, 7)], [ways_loop(n) for n in range(1, 7)])
    print("\n--- Call counts (prediction: naive = 2*ways(n)-1) ---")
    print(f"{'n':>3} {'naive calls':>12} {'predicted':>10} {'memo calls':>11}")
    for n in (10, 20, 25, 30):
        ways_memo.cache_clear()
        calls = 0; r = ways_naive(n); cn = calls
        calls = 0; ways_memo(n); cm = calls
        print(f"{n:>3} {cn:>12} {2*r-1:>10} {cm:>11}")
    print("\n--- n = 1000 ---")
    print("recursion limit:", sys.getrecursionlimit())
    ways_memo.cache_clear()
    try:
        calls = 0; v = ways_memo(1000); print("memo(1000) OK, calls", calls)
    except RecursionError as e:
        print("memo(1000) -> RecursionError:", e)
    sys.setrecursionlimit(5000)
    ways_memo.cache_clear(); calls = 0
    v = ways_memo(1000)
    print("after setrecursionlimit(5000): memo calls =", calls, "| digits:", len(str(v)))
    sys.setrecursionlimit(1000)
    s = time.perf_counter(); lv = ways_loop(1000); t = time.perf_counter() - s
    print("loop(1000) == memo(1000):", lv == v, f"| loop time {t*1e6:.1f} microseconds")
    ways_memo.cache_clear()
    sys.setrecursionlimit(5000)
    s = time.perf_counter(); ways_memo(1000); tm = time.perf_counter() - s
    print(f"memo(1000) time (cold cache) {tm*1e6:.1f} microseconds")
    est = 2 * lv - 1
    print("naive(1000) would need 2*ways(1000)-1 calls, a number with", len(str(est)), "digits -> not run")
    sys.setrecursionlimit(1000)
    try:
        ways_memo.cache_clear(); ways_memo(3000)
    except RecursionError:
        print("memo(3000) with limit 1000 -> RecursionError again")
    print("loop(100000) computed with no recursion, result has", ways_loop(100000).bit_length(), "bits")
