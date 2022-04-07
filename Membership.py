#!/usr/bin/env python3

"""
A collection of common membership functions for fuzzy-logic.
"""


def gbell(x: float, a: float, b: float, c: float) -> float:
    """generalized bell function"""
    return 1 / (1 + pow(abs((x-c)/a), 2 * b))


def impulse(x: float) -> float:
    """Kroneker delta function"""
    return 1.0 if abs(x) < 1e-2 else 0.0


def z_sat(x: float, a: float, b: float) -> float:
    """Z-shape saturating function"""
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    elif a < x <= (a+b)/2:
        return 1 - (2 * pow((x-a)/(b-a), 2))
    else:
        return 2 * pow((x-b)/(b-a), 2)


def s_sat(x: float, a: float, b: float) -> float:
    """S-shape saturating function"""
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    elif a < x <= (a+b)/2:
        return 2 * pow((x-a)/(b-a), 2)
    else:
        return 1 - (2 * pow((x-b)/(b-a), 2))
