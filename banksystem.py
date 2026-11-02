def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def prime_generator():
    "Infinite generator that yields prime numbers in order."
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


def nth_prime(n):
    "Return the n-th prime (1-based) using the generator."
    if n < 1:
        raise ValueError("n must be >= 1")
    for index, prime in enumerate(prime_generator(), start=1):
        if index == n:
            return prime


if __name__ == "__main__":
    gen = prime_generator()
    print("First 10 primes:", [next(gen) for _ in range(10)])
    print("10th prime:", nth_prime(10))   # 29