import time, io
def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text
def build_join(parts):
    return ";".join(parts) + ";"
def build_fstring_plus(parts):
    text = ""
    for p in parts:
        text += f"{p};"
    return text
def build_fstring_join(parts):
    return "".join([f"{p};" for p in parts])
def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p); buf.write(";")
    return buf.getvalue()
def timed(fn, items):
    s = time.perf_counter(); r = fn(items); return r, time.perf_counter() - s
if __name__ == "__main__":
    items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]
    print("=== Complete-the-code program, 3 runs ===")
    tp, tj = [], []
    for run in range(3):
        a, t_plus = timed(build_plus, items); b, t_join = timed(build_join, items)
        tp.append(t_plus); tj.append(t_join)
        print(f"run {run+1}: same text: {a == b} | length: {len(b)} | += time: {t_plus:.4f} s  join time: {t_join:.4f} s")
    print(f"average: += {sum(tp)/3:.4f} s   join {sum(tj)/3:.4f} s")
    print("\n=== Three implementations, average of 3 runs (seconds) ===")
    print(f"{'lines':>8} | {'(a) +=':>9} | {'(b) join':>9} | {'(c) f-string +=':>15} | {'f-string+join':>13} | {'StringIO':>9}")
    for n in (1_000, 10_000, 200_000):
        sub = items[:n]; row = []
        for fn in (build_plus, build_join, build_fstring_plus, build_fstring_join, build_stringio):
            row.append(sum(timed(fn, sub)[1] for _ in range(3)) / 3)
        print(f"{n:>8} | {row[0]:9.5f} | {row[1]:9.5f} | {row[2]:15.5f} | {row[3]:13.5f} | {row[4]:9.5f}")
    r = [build_plus(items[:50]), build_join(items[:50]), build_fstring_plus(items[:50]), build_fstring_join(items[:50]), build_stringio(items[:50])]
    print("\nall five outputs identical:", all(x == r[0] for x in r))
    print("\n=== Defeating the CPython += optimisation (text held by a second reference) ===")
    def build_plus_alias(parts):
        text = ""
        for p in parts:
            alias = text          # second reference -> in-place resize is not allowed
            text += p + ";"
        return text
    for n in (1_000, 10_000, 50_000):
        sub = items[:n]
        t = timed(build_plus_alias, sub)[1]; j = timed(build_join, sub)[1]
        print(f"{n:>8} lines: += with extra reference {t:.4f} s | join {j:.5f} s")
