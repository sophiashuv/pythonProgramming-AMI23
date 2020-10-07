from coprime_chacks import IsCoprime


def coprimes_generator(low, high, first_el):
    while high != 0:
        if IsCoprime.is_coprime(first_el, low):
            high -= 1
            yield (first_el, low)
        low += 1
