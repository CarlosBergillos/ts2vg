from typing import Optional

from ts2vg.graph._natural import _compute_graph
from ts2vg.graph.base import BaseVG


class NaturalVG(BaseVG):
    r"""
    Natural Visibility Graph.

    Transform a time series to a Natural Visibility Graph.

    Parameters
    ----------
    directed : str, None
        If ``None`` make an undirected graph, otherwise, a directed graph with one of the following
        options:

        ``left_to_right`` :
            Edge directions go from left to right according to the series temporal *x* axis.

        ``top_to_bottom`` :
            Edge directions go from top to bottom according to the series *y* axis.

            .. note::
                If both endpoints of an edge have the same *y* value then the direction
                is ambiguous and no consistent direction is guaranteed.

        Default ``None``.

    weighted : str, None
        If ``None`` make an unweighted graph, otherwise, a weighted graph with one of the following
        options (edges going from point :math:`(p_x, p_y)` to point :math:`(q_x, q_y)`):

        ``distance`` :
            Euclidean distance.
            Calculated as:

            .. math::
                \sqrt{(q_x - p_x)^2 \cdot (q_y - p_y)^2}

        ``sq_distance`` :
            Squared Euclidean distance (quicker to compute than regular Euclidean distance).
            Calculated as:

            .. math::
                (q_x - p_x)^2 \cdot (q_y - p_y)^2

        ``v_distance`` :
            Vertical distance.
            Calculated as:

            .. math::
                q_y - p_y

        ``abs_v_distance`` :
            Absolute vertical distance.
            Calculated as:

            .. math::
                \left| q_y - p_y \right|

        ``h_distance``:
            Horizontal distance.
            Calculated as:

            .. math::
                q_x - p_x

        ``abs_h_distance``:
            Absolute horizontal distance.
            Calculated as:

            .. math::
                \left| q_x - p_x \right|

        ``slope`` :
            Slope, in the range (-∞, +∞).
            Calculated as:

            .. math::
                \frac{q_y - p_y}{q_x - p_x}

        ``abs_slope`` :
            Absolute slope, in the range (0, +∞).
            Calculated as:

            .. math::
                \left| \frac{q_y - p_y}{q_x - p_x} \right|

        ``angle`` :
            Slope angle in radians, in the range (-π/2, +π/2).
            Calculated as:

            .. math::
                \arctan \left( \frac{q_y - p_y}{q_x - p_x} \right)

        ``abs_angle`` :
            Absolute slope angle in radians, in the range (0, +π/2).
            Calculated as:

            .. math::
                \arctan \left( \left| \frac{q_y - p_y}{q_x - p_x} \right| \right)

        Default ``None``.

        .. note::
            Asymmetrical weight functions (like ``v_distance``, ``h_distance``, ``slope``,  ``angle``) depend on the edge direction.
            If the graph is undirected, a 'left to right' edge direction is used by default when computing the weights.

    min_weight : float, None
        If provided, only edges with a weight higher than ``min_weight`` (non inclusive) will be included in the final graph.
        The graph must be weighted and the values used for weight will depend on the ``weighted`` parameter.
        This acts a generalization of parametric visibility graphs.
        Default ``None``.

    max_weight : float, None
        If provided, only edges with a weight lower than ``max_weight`` (non inclusive) will be included in the final graph.
        The graph must be weighted and the values used for weight will depend on the ``weighted`` parameter.
        This acts a generalization of parametric visibility graphs.
        Default ``None``.

    References
    ----------
        - Lucas Lacasa et al., "*From time series to complex networks: The visibility graph*", 2008.
        - Xin Lan et al., "*Fast transformation from time series to visibility graphs*", 2015.

    Examples
    --------
    .. code:: python

        from ts2vg import NaturalVG

        ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

        g = NaturalVG()
        g.build(ts)

        edges = g.edges
    """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def _compute_graph(self, only_degrees: bool):
        return _compute_graph(
            self.ts,
            self.xs,
            self._directed,
            self._weighted,
            only_degrees,
            self.min_weight if self.min_weight is not None else float("-inf"),
            self.max_weight if self.max_weight is not None else float("inf"),
        )

    def summary(self):
        self._validate_is_built()

        txt = f"Natural visibility graph"
        if self.is_directed and self.is_weighted:
            txt += " (directed, weighted)"
        elif self.is_directed:
            txt += " (directed)"
        elif self.is_weighted:
            txt += " (weighted)"

        txt += f" with {self.n_vertices} vertices and {self.n_edges} edges."

        return txt
