#!usr/bin/env python3

import numpy as np

from typing import Callable


class CUniverse:
    """defines a continuous universe"""
    def __init__(self, begin, end):
        self.bounds = (begin, end)

    def points(self, n=10_000) -> np.array:
        """:returns n evenly spaced points in the universe"""
        return np.linspace(*self.bounds, num=n)


class CFuzzySet:
    """Continuous fuzzy set"""
    def __init__(self, universe: CUniverse, f: Callable):
        self.u = universe
        self.f = f

    def get_universe(self) -> CUniverse:
        return self.u

    def get_series(self, n=10_000) -> tuple:
        """:returns elements of Self contained in the support set (i.e. membership > 0)"""
        xs = []
        ys = []
        for x in self.u.points(n):
            xs.append(x)
            ys.append(self.f(x))
        return xs, ys

    def get_support(self, n=10_000) -> tuple:
        """:returns elements of Self contained in the support set (i.e. membership > 0)"""
        xs = []
        ys = []
        for x, y in zip(*self.get_series(n)):
            if y > 0.0:
                xs.append(x)
                ys.append(y)
        return xs, ys

    def union(self, other):
        """:returns CFuzzySet representing the union of Self and Other over the universe of Self"""
        return CFuzzySet(self.u, lambda x: max(self.f(x), other.f(x)))

    def inter(self, other):
        """:returns CFuzzySet representing the intersection of Self and Other over the universe of Self"""
        return CFuzzySet(self.u, lambda x: min(self.f(x), other.f(x)))

    def compatibility(self, other) -> float:
        """:returns degree of compatibility of Self with Other"""
        _, ys = self.inter(other).get_series()
        return max(ys)

    def clamped(self, m: float):
        """:returns Self modulated by a given firing strength (compatibility)"""
        return self.inter(CFuzzySet(self.u, lambda _: m))


class DUniverse:
    """defines a discrete universe"""
    def __init__(self, xs):
        self.xs = xs

    def points(self) -> np.array:
        return np.array(self.xs)


class DFuzzySet:
    """Discrete fuzzy set"""
    def __init__(self, elements: list):
        self.mem = dict()
        for k, v in elements:
            self.mem[round(k, 4)] = v

    def get_universe(self) -> DUniverse:
        return DUniverse(list(self.mem.keys()))

    def get_series(self) -> tuple:
        xs = []
        ys = []
        for k, v in self.mem.items():
            xs.append(k)
            ys.append(v)
        return xs, ys

    def union(self, other):
        out = DFuzzySet([])
        for k, v in self.mem.items():
            if k in other.mem:
                out.mem[k] = max(v, other.mem[k])
        return out

    def inter(self, other):
        out = DFuzzySet([])
        for k, v in self.mem.items():
            if k in other.mem:
                out.mem[k] = min(v, other.mem[k])
        return out
