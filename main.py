#!/usr/bin/env python3
import numpy as np

from FuzzySet import CFuzzySet, CUniverse

import matplotlib.pyplot as plt

from Membership import gbell

from Fuzzification import SingletonFuzzifier, Defuzzifier


def main():
    u = CUniverse(-10, 10)

    a_prime = CFuzzySet(u, lambda x: gbell(x, 2, 1, 0))
    b_prime = CFuzzySet(u, lambda x: gbell(x, 2, 1, 5))

    b = SingletonFuzzifier(u).to_fuzzy(5.0)
    a = SingletonFuzzifier(u).to_fuzzy(-5.0)

    plt.plot(*a_prime.get_series(), label="A",                 c="tab:blue")
    plt.plot(*a.get_series(),       label="a (crisp reading)", c="tab:blue")

    plt.plot(*b_prime.get_series(), label="B",                 c="tab:orange")
    plt.plot(*b.get_series(),       label="b (crisp reading)", c="tab:orange")

    # Compute the output activation
    b_prime_activation = b_prime.clamped(b_prime.compatibility(b))
    a_prime_activation = a_prime.clamped(a_prime.compatibility(a))
    total_activation = b_prime_activation.union(a_prime_activation)
    plt.fill_between(*total_activation.get_series(), 0.0, color="lightgray")

    # Compute the output activation centroid
    centroid = Defuzzifier.centroid(total_activation)
    plt.axvline(x=centroid, label="centroid")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
