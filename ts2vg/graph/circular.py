from typing import Optional

from ts2vg.graph._circular import _compute_graph as _compute_graph_pn
from ts2vg.graph.base import VG


class CircularVG(VG):
    r"""
    Circular Visibility Graph.

    Transform a time series to a Circular Visibility Graph.

    Parameters
    ----------
    alpha : float
        Hyperparameter :math:`\alpha` that determines the amount of curvature of the circular arcs.
        Must be in the range (0, +∞).
        Larger values result in flatter circular arcs (smaller arc angles).
        In particular, :math:`\theta = 2 \arctan(1/\alpha)`, where :math:`\theta` is the
        central angle of the resulting circular arcs.
        Default ``1``.

    directed : str, None
        If ``None`` make an undirected graph, otherwise, a directed graph by using one of the following values:
        ``left_to_right``, ``top_to_bottom``.
        See :ref:`Directed graphs` for more information.
        Default ``None``.

    weighted : str, None
        If ``None`` make an unweighted graph, otherwise, a weighted graph by using one of the following values:
        ``distance``, ``sq_distance``, ``v_distance``, ``abs_v_distance``, ``h_distance``, ``abs_h_distance``,
        ``slope``, ``abs_slope``, ``angle``, ``abs_angle``.
        See :ref:`Weighted graphs` for more information.
        Default ``None``.

    min_weight : float, None
        If provided, only edges with a weight higher than ``min_weight`` (non inclusive) will be included in the final graph.
        The graph must be weighted and the values used for weight will depend on the ``weighted`` parameter.
        This acts as a generalization of parametric visibility graphs.
        Default ``None``.

    max_weight : float, None
        If provided, only edges with a weight lower than ``max_weight`` (non inclusive) will be included in the final graph.
        The graph must be weighted and the values used for weight will depend on the ``weighted`` parameter.
        This acts as a generalization of parametric visibility graphs.
        Default ``None``.

    penetrable_limit : int
        If larger than 0, make a limited penetrable visibility graph (LPVG).
        The value for ``penetrable_limit`` indicates the maximum number of data points that are allowed to obstruct the visibility
        between two nodes that can still be connected in the final graph.
        Default ``0`` (regular non-penetrable visibility graph).

    References
    ----------
        - Qi Xuan et al., "*CLPVG: Circular limited penetrable visibility graph as a new network model for time series*", 2021.

    Examples
    --------
    .. code:: python

        from ts2vg import CircularVG

        ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

        g = CircularVG()
        g.build(ts)

        edges = g.edges
    """

    _general_type_name = "Circular Visibility Graph"

    def __init__(self, alpha: float = 1.0, *args, **kwargs):
        self.alpha = alpha
        super().__init__(*args, **kwargs)

    def _compute_graph(self, only_degrees: bool):
        return _compute_graph_pn(
            self.ts,
            self.xs,
            self.alpha,
            self._directed,
            self._weighted,
            only_degrees,
            self.min_weight if self.min_weight is not None else float("-inf"),
            self.max_weight if self.max_weight is not None else float("inf"),
        )
