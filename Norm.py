#!/usr/bin/env python3

class TNorm:
    """Interface for various common T-norm operators"""
    @staticmethod
    def min(x: float, y: float) -> float:
        """:returns the min T-norm of x and y"""
        return min(x, y)

    @staticmethod
    def prod_algebraic(x: float, y: float) -> float:
        """:returns the algebraic product T-norm of x and y"""
        return x * y

    @staticmethod
    def prod_bounded(x: float, y: float) -> float:
        """:returns the bounded product T-norm of x and y"""
        return max(0.0, x + y - 1.0)

    @staticmethod
    def prod_basic(x: float, y: float) -> float:
        """:returns the basic product T-norm of x and y"""
        if x == 1.0:
            return y
        elif y == 1.0:
            return x
        else:
            return 0
