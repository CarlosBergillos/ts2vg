from typing import Optional

from ts2vg.graph._horizontal import _compute_graph as _compute_graph_dc
from ts2vg.graph._horizontal_penetrable import _compute_graph as _compute_graph_pn
from ts2vg.graph.base import BaseVG


class HorizontalVG(BaseVG):
    r"""
    Horizontal Visibility Graph.

    Transform a time series to a Horizontal Visibility Graph.

    Parameters
    ----------
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
        If larger than 0, make a limited penetrable horizontal visibility graph (LPHVG).
        ``penetrable_limit`` indicates the maximum number of data points that are allowed to obstruct the visibility
        between two nodes that will still be connected in the final graph.
        Limited penetrable visibility graphs can be more robust to noise in the time series.
        Default ``0`` (regular non-penetrable visibility graph).

    References
    ----------
        - Lucas Lacasa et al., "*Horizontal visibility graphs: exact results for random time series*", 2009.
        - Xin Lan et al., "*Fast transformation from time series to visibility graphs*", 2015.

    Examples
    --------
    .. code:: python

        from ts2vg import HorizontalVG

        ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

        g = HorizontalVG()
        g.build(ts)

        edges = g.edges

    """

    general_type_name = "Horizontal Visibility Graph"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def _compute_graph(self, only_degrees: bool):
        if self.penetrable_limit == 0:
            return _compute_graph_dc(
                self.ts,
                self.xs,
                self._directed,
                self._weighted,
                only_degrees,
                self.min_weight if self.min_weight is not None else float("-inf"),
                self.max_weight if self.max_weight is not None else float("inf"),
            )
        else:
            return _compute_graph_pn(
                self.ts,
                self.xs,
                self._directed,
                self._weighted,
                only_degrees,
                self.min_weight if self.min_weight is not None else float("-inf"),
                self.max_weight if self.max_weight is not None else float("inf"),
                self.penetrable_limit,
            )

        return
