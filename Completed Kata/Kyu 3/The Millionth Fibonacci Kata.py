def fib(n):
    if n >= 0:
        return fib_(1, 0, 0, 1, n)
    if n < 0:
        a, b = 0, 1
        for i in range(0, n, -1):
            a, b = b - a, a
        return a
#oof
def fib_(k, l, m, n, count):
    if count == 0:
        return l
    if count % 2 == 0:
        return fib_(k, l, m * m + n * n, n * n + 2 * m * n, count / 2)
    else:
        return fib_(l * n + k * n + k * m, l * m + k * n, m, n, count - 1)
