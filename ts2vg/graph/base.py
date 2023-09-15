import numpy as np
from numpy.typing import ArrayLike, NDArray

from typing import Optional, List, Tuple, Union

from ts2vg.graph.summary import simple_summary


# TypeAlias in Python >= 3.10
UnweightedEdgeList = List[Tuple[int, int]]
WeightedEdgeList = List[Tuple[int, int, float]]
EdgeList = Union[UnweightedEdgeList, WeightedEdgeList]


_DIRECTED_OPTIONS = {
    None: 0,
    "left_to_right": 1,
    "top_to_bottom": 2,
}

_WEIGHTED_OPTIONS = {
    None: 0,
    "distance": 1,
    "sq_distance": 2,
    "v_distance": 3,
    "abs_v_distance": 4,
    "h_distance": 5,
    "abs_h_distance": 6,
    "slope": 7,
    "abs_slope": 8,
    "angle": 9,
    "abs_angle": 10,
    "num_penetrations": 11,
}

class NotBuiltError(Exception):
    """
    Exception class to raise if certain graph attributes or methods are accessed before
    the graph has been built.
    """


class VG:
    """
    Abstract class for a visibility graph (VG).

    .. caution::
        Should not be used directly, use one of the subclasses instead,
        e.g :class:`ts2vg.NaturalVG` or :class:`ts2vg.HorizontalVG`.
    """

    _general_type_name = "Visibility Graph"

    def __init__(
        self,
        *,
        directed: Optional[str] = None,
        weighted: Optional[str] = None,
        min_weight: Optional[float] = None,
        max_weight: Optional[float] = None,
        penetrable_limit: int = 0,
    ):
        self.ts: Optional[NDArray[np.float64]] = None
        """1D array of the time series. ``None`` if the graph has not been built yet."""

        self.xs: Optional[NDArray[np.float64]] = None
        """1D array of the X coordinates of the time series. ``None`` if the graph has not been built yet."""

        self._m: Optional[int] = None
        self._edges: Optional[EdgeList] = None
        self._degrees: Optional[NDArray[np.uint32]] = None
        self._degrees_in: Optional[NDArray[np.uint32]] = None
        self._degrees_out: Optional[NDArray[np.uint32]] = None

        if directed not in _DIRECTED_OPTIONS:
            raise ValueError(
                f"Invalid 'directed' parameter: {directed}. Must be one of {list(_DIRECTED_OPTIONS.keys())}"
            )

        self.directed = directed
        """`str` indicating the strategy used for the edge directions (same as passed to the constructor). ``None`` if the graph is undirected."""
        self._directed = _DIRECTED_OPTIONS[directed]

        if weighted not in _WEIGHTED_OPTIONS:
            raise ValueError(
                f"Invalid 'weighted' parameter: {weighted}. Must be one of {list(_WEIGHTED_OPTIONS.keys())}."
            )

        self.weighted = weighted
        """`str` indicating the strategy used for the edge weights (same as passed to the constructor). ``None`` if the graph is unweighted."""
        self._weighted = _WEIGHTED_OPTIONS[weighted]

        if weighted is None and min_weight is not None:
            raise ValueError("'min_weight' can only be used in weighted graphs.")

        self.min_weight = min_weight

        if weighted is None and max_weight is not None:
            raise ValueError("'max_weight' can only be used in weighted graphs.")

        self.max_weight = max_weight

        if penetrable_limit < 0:
            raise ValueError(f"'penetrable_limit' cannot be negative (got {penetrable_limit}).")

        self.penetrable_limit = penetrable_limit

    def _validate_is_built(self) -> None:
        if self.ts is None or self._edges is None:
            raise NotBuiltError("Visibility graph has has not been built yet, call '.build(...)' first.")

    def build(self, ts: ArrayLike, xs: ArrayLike = None, only_degrees: bool = False):
        """
        Compute and build the visibility graph for the given time series.

        Parameters
        ----------
        ts : 1D array like
            Input time series.

        xs : 1D array like, optional
            X coordinates for the time series.
            Length of ``xs`` must match length of ``ts``.

            If not provided, ``[0, 1, 2...]`` will be used.

        only_degrees : bool
            If ``True`` only compute the graph degrees, otherwise compute the whole graph.
            Default ``False``.

        Returns
        -------
            self
        """
        self.ts = np.asarray(ts, dtype=np.float64)

        if self.ts.ndim != 1:
            raise ValueError("Input time series must be one-dimensional.")

        if xs is None:
            self.xs = np.arange(len(ts), dtype=np.float64)
        else:
            if len(xs) != len(self.ts):
                raise ValueError(f"Length of 'xs' ({len(xs)}) does not match length of 'ts' ({len(self.ts)}).")

            self.xs = np.asarray(xs, dtype=np.float64)

            if self.xs.ndim != 1:
                raise ValueError("Input 'xs' series must be one-dimensional.")

            if np.any(np.diff(self.xs) <= 0):
                raise ValueError("Input 'xs' series must be monotonically increasing.")

        if only_degrees and self.is_weighted:
            raise ValueError("Building with 'only_degrees' is only supported for unweighted graphs.")

        if len(ts) == 0:
            # empty time series results in an empty graph
            self._edges = None if only_degrees else []
            self._degrees_in = np.zeros(0, dtype=np.uint32)
            self._degrees_out = np.zeros(0, dtype=np.uint32)
            self._degrees = np.zeros(0, dtype=np.uint32)
            return self

        self._edges, self._degrees_in, self._degrees_out = self._compute_graph(only_degrees)
        self._degrees = self._degrees_in + self._degrees_out

        if only_degrees:  # `_compute_graph` doesn't return valid edges when only_degrees=True
            self._edges = None

        return self

    @property
    def is_directed(self) -> bool:
        """``True`` if the graph is directed, ``False`` otherwise."""
        return self.directed is not None

    @property
    def is_weighted(self) -> bool:
        """``True`` if the graph is weighted, ``False`` otherwise."""
        return self.weighted is not None

    @property
    def n_vertices(self) -> int:
        """
        Number of vertices (nodes) in the graph.
        """
        self._validate_is_built()

        return self.ts.size

    @property
    def n_edges(self) -> int:
        """
        Number of edges (links) in the graph.
        """
        self._validate_is_built()

        if self._m is None:
            if self._edges is not None:
                self._m = len(self._edges)
            elif self._degrees is not None:
                self._m = np.sum(self._degrees, dtype=int) // 2
            else:
                raise NotBuiltError("Cannot access graph edges, use 'build' first.")

        return self._m

    @property
    def edges(self) -> EdgeList:
        """
        List of edges (links) of the graph.

        If the graph is unweighted, a list of tuple pairs `(source_node, target_node)`.
        If the graph is weighted, an iterable of tuple triplets `(source_node, target_node, weight)`.

        Nodes are identified using an integer from 0 to *n*-1 assigned sequentially in the same order as the input time series.
        """
        self._validate_is_built()

        return self._edges

    @property
    def edges_unweighted(self) -> UnweightedEdgeList:
        """
        List of edges (links) of the graph without including the weights.

        A list of tuple pairs `(source_node, target_node)`.
        For unweighted graphs this is the same as :attr:`edges`.

        Nodes are identified using an integer from 0 to *n*-1 assigned sequentially in the same order as the input time series.
        """
        self._validate_is_built()

        if not self.is_weighted:
            return self.edges

        return [(source_node, target_node) for (source_node, target_node, _) in self.edges]

    @property
    def weights(self) -> Optional[List[float]]:
        """
        Weights of the edges of the graph.

        A list of the weights of the edges of the graph (listed in the same order as in :attr:`edges`).
        ``None`` if the graph is unweighted.
        """
        self._validate_is_built()

        if self.weighted is None:
            return None

        return [weight for (_, _, weight) in self.edges]

    @property
    def degrees(self) -> NDArray[np.uint32] | NDArray[np.intp]:
        """
        Degree sequence of the graph.

        An array of degree values for each node in the graph, in the same order as the input time series.
        """
        if self._degrees is not None:
            pass
        elif self._edges is not None:
            edges_array = np.asarray(self.edges_unweighted, dtype=np.uint32)
            self._degrees = np.bincount(edges_array.flat)
        else:
            raise NotBuiltError("Cannot access graph edges, use 'build' first.")

        return self._degrees

    @property
    def degrees_in(self):
        self._validate_is_built()

        return self._degrees_in

    @property
    def degrees_out(self):
        self._validate_is_built()

        return self._degrees_out

    @property
    def degree_counts(self) -> tuple[NDArray, NDArray[intp]]:
        """
        Degree counts of the graph.

        Two arrays `ks`, `cs` are returned.
        `cs[i]` is the number of nodes in the graph that have degree `ks[i]`.

        The count of any other degree value not listed in `ks` is 0.
        """
        self._validate_is_built()

        ks, cs = np.unique(self.degrees, return_counts=True)

        return ks, cs

    @property
    def degree_distribution(self):
        """
        Degree distribution of the graph.

        Two arrays `ks`, `ps` are returned.
        `ps[i]` is the empirical probability that a node in the graph has degree `ks[i]`.

        The probability for any other degree value not listed in `ks` is 0.
        """
        self._validate_is_built()

        ks, cs = self.degree_counts
        ps = cs / self.n_vertices

        return ks, ps

    def adjacency_matrix(self, triangle="both", use_weights=False, no_weight_value=np.nan):
        """
        Adjacency matrix of the graph.

        Parameters
        ----------
        triangle : str
            One of ``'lower'`` (uses the lower triangle of the matrix),
            ``'upper'`` (uses the upper triangle of the matrix)
            or ``'both'`` (uses both).
            Only applicable for undirected graphs.

            Default ``'both'``.

        use_weights : bool
            If ``True``, return an adjacency matrix containing the edge weights,
            otherwise return a binary adjacency matrix.
            Only applicable for weighted graphs.

            Default ``False``.

        no_weight_value : float
            The value used in the matrix for the cases where the nodes are not connected.
            Only applicable for weighted graphs and when using ``use_weights=True``.

            Default ``np.nan``.

        Returns
        -------
        2D array
            Adjacency matrix of the graph.

        """
        self._validate_is_built()

        if triangle != "both" and self.is_directed:
            raise ValueError(f"'triangle' value '{triangle}' not valid for directed graphs.")

        if triangle not in ["lower", "upper", "both"]:
            raise ValueError(f"'triangle' must be one of 'lower', 'upper', 'both'. Got '{triangle}'.")

        if use_weights and not self.is_weighted:
            raise ValueError(f"'use_weights=True' only valid for weighted graphs.")

        e = np.asarray(self.edges_unweighted, dtype=np.uint32)
        w = self.weights

        if self.is_weighted and use_weights:
            m = np.full((self.n_vertices, self.n_vertices), fill_value=no_weight_value, dtype=np.float64)
            if self.is_directed:
                m[e[:, 0], e[:, 1]] = w
            else:
                if triangle == "both" or triangle == "upper":
                    m[e[:, 0], e[:, 1]] = w

                if triangle == "both" or triangle == "lower":
                    m[e[:, 1], e[:, 0]] = w
        else:
            m = np.zeros((self.n_vertices, self.n_vertices), dtype="uint8")
            if self.is_directed:
                m[e[:, 0], e[:, 1]] = 1
            else:
                if triangle == "both" or triangle == "upper":
                    m[e[:, 0], e[:, 1]] = 1

                if triangle == "both" or triangle == "lower":
                    m[e[:, 1], e[:, 0]] = 1

        return m

    def as_igraph(self):
        """
        Return an `igraph <https://igraph.org/python/>`_ graph object corresponding to this graph.

        The ``igraph`` package is required.
        """
        self._validate_is_built()

        from igraph import Graph

        g = Graph(
            n=self.n_vertices,
            edges=self.edges_unweighted,
            vertex_attrs={"name": range(self.n_vertices)},
            edge_attrs={"weight": self.weights} if self.is_weighted else {},
            directed=self.is_directed,
        )

        return g

    def as_networkx(self):
        """
        Return a `NetworkX <https://networkx.github.io/>`_ graph object corresponding to this graph.

        The ``networkx`` package is required.
        """
        self._validate_is_built()

        from networkx import DiGraph, Graph

        if self.is_directed:
            g = DiGraph()
        else:
            g = Graph()

        g.add_nodes_from(range(self.n_vertices))

        if self.is_weighted:
            g.add_weighted_edges_from(self.edges)
        else:
            g.add_edges_from(self.edges)

        return g

    def as_snap(self):
        """
        Return a `SNAP <https://snap.stanford.edu/snappy/>`_ graph object corresponding to this graph.

        The ``snap`` package is required.
        """
        self._validate_is_built()

        from snap import TUNGraph, TNGraph

        if self.is_weighted:
            raise NotImplementedError("SNAP weighted graphs not currently supported.")

        if self.is_directed:
            g = TNGraph.New(self.n_vertices, self.n_edges)
        else:
            g = TUNGraph.New(self.n_vertices, self.n_edges)

        for i in range(self.n_vertices):
            g.AddNode(i)

        for e in self.edges:
            g.AddEdge(*e)

        return g

    def node_positions(self):
        """
        Dictionary with nodes as keys and positions *(x, y)* as values.
        """

        return {i: (self.xs[i], self.ts[i]) for i in range(self.n_vertices)}

    def summary(self, prints: bool = True, title: str = "Visibility Graph"):
        """
        Prints (or returns) a simple text summary describing the visibility graph.

        Parameters
        ----------
        prints : bool
            If ``True`` prints the summary, otherwise returns the summary as a string.
            Default ``True``.

        title : str
            Title for the table. Default is 'Visibility Graph'.

        Returns
        -------
        str
            A string containing the short summary (only if ``prints=False``).
        """
        text = simple_summary(self, title=title)

        if prints:
            print(text)
        else:
            return text

    # def _compute_graph(self):
    #     raise NotImplementedError()
