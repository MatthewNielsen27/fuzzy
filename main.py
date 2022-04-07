#!/usr/bin/env python3

"""
Driver code for Fuzzy project.
"""

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt

from FuzzySet import CFuzzySet, CUniverse
from Fuzzification import SingletonFuzzifier
from Membership import z_sat, s_sat
from Norm import TNorm


def main():
    # [Part 0] preamble
    # --
    u = CUniverse(-5, 5)

    x_small = CFuzzySet(u, lambda x: z_sat(x, -2, 2))
    x_large = CFuzzySet(u, lambda x: s_sat(x, -2, 2))

    y_small = CFuzzySet(u, lambda x: z_sat(x, -5, 5))
    y_large = CFuzzySet(u, lambda x: s_sat(x, -5, 5))

    # [Part 1] plotting the antecedents
    # --
    _, ax = plt.subplots(nrows=2, ncols=1)

    plt.suptitle("Two-Input Sugeno Fuzzy Model MFs")

    ax[0].plot(*x_small.get_series(), label="x Small")
    ax[0].plot(*x_large.get_series(), label="x Large")
    ax[0].set_xlabel("X")
    ax[0].set_ylabel("Degree of Membership")

    ax[0].legend()

    ax[1].plot(*y_small.get_series(), label="y Small")
    ax[1].plot(*y_large.get_series(), label="y Large")
    ax[1].set_xlabel("Y")
    ax[1].set_ylabel("Degree of Membership")
    ax[1].legend()

    plt.tight_layout()
    plt.legend()
    plt.savefig('input.png')

    # [Part 2] computing the surface
    # --
    def fuzzy_inference(x: float, y: float):
        """
        :param x is a crisp value x of X
        :param y is a crisp value y of Y
        :returns an inference of Z using a Sugeno Fuzzy Model

        if x_small and y_small -> z = -x + y + 1
        if x_small and y_large -> z = -y + 3
        if x_large and y_small -> z = -x + 3
        if x_large and y_large -> z = x + y + 2
        """
        x_fuzzy = SingletonFuzzifier(u).to_fuzzy(x)
        y_fuzzy = SingletonFuzzifier(u).to_fuzzy(y)

        ws = [
            # Antecedent 1: if x_small and y_small
            TNorm.min(
                x_small.compatibility(x_small.inter(x_fuzzy)),
                y_small.compatibility(y_small.inter(y_fuzzy)),
            ),
            # Antecedent 2: if x_small and y_large
            TNorm.min(
                x_small.compatibility(x_small.inter(x_fuzzy)),
                y_large.compatibility(y_large.inter(y_fuzzy)),
            ),
            # Antecedent 3: if x_large and y_small
            TNorm.min(
                x_large.compatibility(x_large.inter(x_fuzzy)),
                y_small.compatibility(y_small.inter(y_fuzzy)),
            ),
            # Antecedent 1: if x_large and y_large
            TNorm.min(
                x_large.compatibility(x_large.inter(x_fuzzy)),
                y_large.compatibility(y_large.inter(y_fuzzy)),
            )
        ]

        zs = [
            # Consequence 1: z = -x + y + 1
            -x + y + 1,
            # Consequence 2: z = -y + 3
            -y + 3,
            # Consequence 3: z = -x + 3
            -x + 3,
            # Consequence 4: z = x + y + 2
            x + y + 2
        ]

        return sum([w * z for w, z in zip(ws, zs)]) / sum(ws)

    # Note: you can increase the number of points here
    n = 15
    points = []

    # Generate the cartesian product of the 2 input variables
    # (in this case they come from the same universe)
    for x in u.points(n=n):
        for y in u.points(n=n):
            if len(points) % 100 == 0:
                print(f'computed {len(points)} out of {n*n}')

            # Compute the fuzzy inference and store the point of the surface
            points.append((x, y, fuzzy_inference(x, y)))

    # save to disk because the previous computation was expensive and we will
    # most likely fiddle with plotting multiple times
    with open('surface.csv', 'w') as f:
        for point in points:
            f.write(f"{point[0]},{point[1]},{point[2]}\n")

    # [Part 3] plotting the surface
    # --
    plot_suface('surface.csv', shape=(n, n))


def plot_suface(filename: str, shape: tuple):
    xs = []
    ys = []
    zs = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            tokens = line.split(',')
            xs.append(float(tokens[0]))
            ys.append(float(tokens[1]))
            zs.append(float(tokens[2]))

    xs = np.array(xs).reshape(shape)
    ys = np.array(ys).reshape(shape)
    zs = np.array(zs).reshape(shape)

    plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot_surface(xs, ys, zs, cmap=cm.Spectral, linewidth=0, antialiased=False)

    ax.set_xlabel(f'X')
    ax.set_ylabel(f'Y')
    ax.set_zlabel(f'Z')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
