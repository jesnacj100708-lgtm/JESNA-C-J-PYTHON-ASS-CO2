import timeit
def add_item_buggy(item, order=[]):
    order.append(item)
    return order
def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order
def bill(prices, gst_rate=0.05):
    """Return TWO values (a tuple): total and GST."""
    total = sum(prices)
    return total, round(total * gst_rate, 2)
def make_order():
    """Closure design: the list lives inside the outer function."""
    order = []
    def add(item):
        order.append(item)
        return order
    return add
counter = 0
def count_global():
    global counter
    counter += 1
def outer():
    n = 0
    def inner():
        nonlocal n
        n += 1
        return n
    inner(); inner()
    return n
if __name__ == "__main__":
    print("--- Complete the Code ---")
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
    print("add_item.__defaults__       =", add_item.__defaults__)
    print("\n--- Three customers in sequence (fixed design) ---")
    c1 = add_item("Tea"); add_item("Samosa", c1)
    c2 = add_item("Coffee"); add_item("Dosa", c2); add_item("Vada", c2)
    c3 = add_item("Juice")
    print("customer 1:", c1); print("customer 2:", c2); print("customer 3:", c3)
    print("independent lists:", c1 is not c2 and c2 is not c3)
    print("\n--- Parameters ---")
    print(bill([20, 35, 45]), "| keyword:", bill(prices=[20, 35, 45], gst_rate=0.18))
    total, gst = bill([20, 35, 45]); print("unpacked total =", total, " gst =", gst)
    print("\n--- Scope ---")
    x = "global x"
    def local_demo():
        x = "local x"
        return x
    print(local_demo(), "|", x)
    count_global(); count_global(); print("global counter after 2 calls:", counter)
    print("nonlocal n after 2 calls:", outer())
    def no_global():
        try:
            counter += 1
        except UnboundLocalError as e:
            return "UnboundLocalError: " + str(e)
    print(no_global())
    print("\n--- Closure design: three customers ---")
    a, b = make_order(), make_order()
    a("Tea"); a("Samosa"); b("Coffee")
    print("closure a:", a("Vada"), "| closure b:", b("Dosa"))
    N = 300_000
    t1 = timeit.timeit(lambda: add_item("Tea"), number=N)
    t2 = timeit.timeit(lambda: add_item("Tea", []), number=N)
    f = make_order()
    t3 = timeit.timeit(lambda: f("Tea"), number=N)
    print(f"\ntime per call: default None {t1/N*1e9:.0f} ns | explicit list {t2/N*1e9:.0f} ns | closure {t3/N*1e9:.0f} ns")
