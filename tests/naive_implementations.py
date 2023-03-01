"""
Naive pure-Python implementations of visibility graph algorithms for time series.

The implementations here do intentionally not make use of any optimizations.
They aim to be as simple and clear as possible, and to be used as a reference during tests.
"""


def natural_visibility_graph(ts, xs, penetrable_limit=0):
    n = len(ts)
    edges = []

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            penetrations = 0

            for i_c in range(i_a + 1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                if y_c >= y_b + (y_a - y_b) * (x_b - x_c) / (x_b - x_a):
                    penetrations += 1

                    if penetrations > penetrable_limit:
                        break
            else:
                edges.append((i_a, i_b))

    return edges


def horizontal_visibility_graph(ts, xs, penetrable_limit=0):
    n = len(ts)
    edges = []

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            penetrations = 0

            for i_c in range(i_a + 1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                if y_c >= min(y_a, y_b):
                    penetrations += 1

                    if penetrations > penetrable_limit:
                        break
            else:
                edges.append((i_a, i_b))

    return edges


def circular_visibility_graph(ts, xs, alpha):
    from math import pi, atan, atan2

    def angle_between(v1, v2):
        """Returns the angle in radians between vectors 'v1' and 'v2'."""
        angle1 = atan2(v1[1], v1[0])
        angle2 = atan2(v2[1], v2[0])

        angle_diff = angle2 - angle1

        if angle_diff < 0:
            angle_diff += 2 * pi

        return angle_diff

    n = len(ts)
    edges = []

    threshold_angle = pi - atan(1 / alpha)

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            for i_c in range(i_a + 1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                v1 = (x_a - x_c, y_a - y_c)
                v2 = (x_b - x_c, y_b - y_c)

                angle = angle_between(v1, v2)

                if angle < threshold_angle:
                    break
            else:
                edges.append((i_a, i_b))

    return edges



def circular_visibility_graph_2(ts, xs, alpha):
    from math import sqrt

    def get_arc_y(x0, y0, x1, y1, x, a):
        u = sqrt(-4 * (x - x1) * (-a * y0 + x - x0) - 4 * y1 * (a * (x - x0) + y0) + (a * (x1 - x0) + y0 + y1)**2)
        v = - a * x0 + a * x1 + y0 + y1

        y_arc = 0.5 * (+u + v)

        return y_arc

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

                y_arc = get_arc_y(x_a, y_a, x_b, y_b, x_c, alpha)

                if y_c >= y_arc:
                    break
            else:
                edges.append((i_a, i_b))

    return edges



def circular_visibility_graph_3(ts, xs, alpha):
    from math import pi, atan, sin, cos

    n = len(ts)
    edges = []

    rotation_angle = pi - atan(1 / alpha)

    print(rotation_angle * 180 / pi)

    for i_a in range(n - 1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        lines = []

        for i_b in range(i_a + 1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            for (line_slope, line_intercept) in lines:
                y_b_line = line_slope * x_b + line_intercept
                
                if y_b_line > y_b:
                    break

            else:
                edges.append((i_a, i_b))
            
            # rotate point (x_a, y_a) around (x_b, y_b) by rotation_angle radians
            x_p = cos(rotation_angle) * (x_a - x_b) - sin(rotation_angle) * (y_a - y_b) + x_b
            y_p = sin(rotation_angle) * (x_a - x_b) + cos(rotation_angle) * (y_a - y_b) + y_b

            if x_p <= x_b:
                # line rotated past x_b and is pointing backwards, will not obstruct any upcoming point.
                continue
            
            # y = m x + n
            # y_b = m x_b + n
            # n = y_b - m x_b
                
            line_slope = (y_p - y_b) / (x_p - x_b)
            line_intercept = y_b - line_slope * x_b

            lines.append((line_slope, line_intercept))

            # TODO: remove any previous lines that become redundant.

    return edges