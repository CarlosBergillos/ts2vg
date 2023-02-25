"""
Naive pure-Python implementations of visibility graph algorithms for time series.

The implementations here do intentionally not make use of any optimizations.
They aim to be as simple and clear as possible, and to be used as a reference during tests.
"""


def natural_visibility_graph(ts, xs):
    n = len(ts)
    edges = []

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            for i_c in range(i_a + 1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                if y_c >= y_b + (y_a - y_b) * (x_b - x_c) / (x_b - x_a):
                    break
            else:
                edges.append((i_a, i_b))

    return edges


def horizontal_visibility_graph(ts, xs):
    n = len(ts)
    edges = []

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            for i_c in range(i_a + 1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                if y_c >= min(y_a, y_b):
                    break
            else:
                edges.append((i_a, i_b))

    return edges
