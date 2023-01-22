Graph options
=============

Directed graphs
---------------

Directed graphs can be obtained by using the ``directed`` parameter in the graph constructor.
If this parameter is ``None``, an undirected graph will be produced.
Otherwise, for a directed graph, ``directed`` can take one of the following values:

``left_to_right`` :
    Edge directions go from left to right according to the series temporal *x* axis.

``top_to_bottom`` :
    Edge directions go from top to bottom according to the series *y* axis.

    .. note::
        If both endpoints of an edge have the exact same *y* value then the direction
        is ambiguous and no consistent direction is guaranteed.

Weighted graphs
---------------

Weighted graphs can be obtained by using the ``weighted`` parameter in the graph constructor.
If this parameter is ``None``, an unweighted graph will be produced.
Otherwise, for a weighted graph, ``weighted`` can take one of the following values
(assuming directed edges going from point :math:`(x_i, y_i)` to point :math:`(x_j, y_j)`):


``distance`` :
    Euclidean distance.
    Calculated as:

    .. math::
        \sqrt{(x_j - x_i)^2 \cdot (y_j - y_i)^2}

``sq_distance`` :
    Squared Euclidean distance (quicker to compute than regular Euclidean distance).
    Calculated as:

    .. math::
        (x_j - x_i)^2 \cdot (y_j - y_i)^2

``v_distance`` :
    Vertical distance.
    Calculated as:

    .. math::
        y_j - y_i

``abs_v_distance`` :
    Absolute vertical distance.
    Calculated as:

    .. math::
        \left| y_j - y_i \right|

``h_distance``:
    Horizontal distance.
    Calculated as:

    .. math::
        x_j - x_i

``abs_h_distance``:
    Absolute horizontal distance.
    Calculated as:

    .. math::
        \left| x_j - x_i \right|

``slope`` :
    Slope, in the range (-∞, +∞).
    Calculated as:

    .. math::
        \frac{y_j - y_i}{x_j - x_i}

``abs_slope`` :
    Absolute slope, in the range (0, +∞).
    Calculated as:

    .. math::
        \left| \frac{y_j - y_i}{x_j - x_i} \right|

``angle`` :
    Slope angle in radians, in the range (-π/2, +π/2).
    Calculated as:

    .. math::
        \arctan \left( \frac{y_j - y_i}{x_j - x_i} \right)

``abs_angle`` :
    Absolute slope angle in radians, in the range (0, +π/2).
    Calculated as:

    .. math::
        \arctan \left( \left| \frac{y_j - y_i}{x_j - x_i} \right| \right)

.. note::
    Asymmetrical weight functions (like ``v_distance``, ``h_distance``, ``slope``,  ``angle``) depend on the edge direction,
    the direction specified in the ``directed`` parameter is used.
    If the graph is undirected, a 'left to right' edge direction is used by default.
