class b:
    c = 100

    def __init__(self):
        pass


class f:
    a, b1 = None, None

    def __init__(self, a, b1):
        self.a = 1
        b1 = 2


ab = 10
k = ab
print(k)

p = f(10, k)

print(k, ab)
