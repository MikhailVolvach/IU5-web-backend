def makeCounter():
    k = -1
    def add():
        nonlocal k
        k += 1
        return k
    return add