#!/usr/bin/env python3

from FuzzySet import CUniverse, CFuzzySet
from Membership import impulse


class SingletonFuzzifier:
    """Input fuzzifier using the singleton method"""
    def __init__(self, u: CUniverse):
        self.u = u

    def to_fuzzy(self, y_not: float) -> CFuzzySet:
        return CFuzzySet(self.u, lambda y: impulse(y - y_not))


class Defuzzifier:
    """interface for de-fuzzification"""

    @staticmethod
    def centroid(s: CFuzzySet, n:int = 10_000) -> float:
        """de-fuzzifies S using the centroid method"""
        span = float(abs(s.u.bounds[1] - s.u.bounds[0]))
        xs, ys = s.get_series(n=100_000)
        # Compute the top and bottom integrals for the centroid calculation
        dx = span / n
        area_bot = sum(y * dx for y in ys)
        area_top = sum(y * dx * x for x, y in zip(xs, ys))

        return area_top / area_bot
