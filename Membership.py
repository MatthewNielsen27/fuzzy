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


def z_sat(x: float, z1: float, z2: float) -> float:
    """Z-shape saturating function"""
    if x < z1:
        return 1.0
    elif x > z2:
        return 0.0
    else:
        m = (0 - 1) / (z2 - z1)
        b = -m * z2
        return (m * x) + b


def s_sat(x: float, z1: float, z2: float) -> float:
    """S-shape saturating function"""
    if x < z1:
        return 0.0
    elif x > z2:
        return 0.0
    else:
        m = (1 - 0) / (z2 - z1)
        b = -m * z2
        return (m * x) + b
