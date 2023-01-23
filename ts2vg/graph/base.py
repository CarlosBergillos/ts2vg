import numpy as np
from typing import Optional

_DIRECTED_OPTIONS = {
    None: 0,
    "left_to_right": 1,
    "top_to_bottom": 2,
}

_WEIGHTED_OPTIONS = {
    None: {
        "code": 0,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "distance": {
        "code": 1,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "sq_distance": {
        "code": 2,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "v_distance": {
        "code": 3,
        "x_symmetric": True,
        "y_symmetric": False,
    },
    "abs_v_distance": {
        "code": 4,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "h_distance": {
        "code": 5,
        "x_symmetric": False,
        "y_symmetric": True,
    },
    "abs_h_distance": {
        "code": 6,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "slope": {
        "code": 7,
        "x_symmetric": False,
        "y_symmetric": False,
    },
    "abs_slope": {
        "code": 8,
        "x_symmetric": True,
        "y_symmetric": True,
    },
    "angle": {
        "code": 9,
        "x_symmetric": False,
        "y_symmetric": False,
    },
    "abs_angle": {
        "code": 10,
        "x_symmetric": True,
        "y_symmetric": True,
    },
}


class NotBuiltError(Exception):
    """
    Exception class to raise if certain graph attributes or methods are accessed before
    the graph has been built.
    """


class BaseVG:
    """
    Abstract class for a visibility graph (VG).

    .. caution::
        Should not be used directly, use one of the subclasses instead,
        e.g :class:`ts2vg.NaturalVG` or :class:`ts2vg.HorizontalVG`.
    """

    def __init__(
        self,
        *,
        directed: Optional[str] = None,
        weighted: Optional[str] = None,
        min_weight: Optional[float] = None,
        max_weight: Optional[float] = None,
        dual_perspective: bool = False,
    ):
        self.ts = None
        """1D array of the time series. ``None`` if the graph has not been built yet."""

        self.xs = None
        """1D array of the X coordinates of the time series. ``None`` if the graph has not been built yet."""

        self._m = None
        self._edges = None
        self._degrees = None
        self._degrees_in = None
        self._degrees_out = None

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
        self._weighted = _WEIGHTED_OPTIONS[weighted]["code"]

        if weighted is None and min_weight is not None:
            raise ValueError("'min_weight' can only be used in weighted graphs.")

        self.min_weight = min_weight

        if weighted is None and max_weight is not None:
            raise ValueError("'max_weight' can only be used in weighted graphs.")

        self.max_weight = max_weight

        if dual_perspective and directed == "top_to_bottom":
            # Top-to-bottom is ambiguous in dual-perspective visibility graphs.
            raise ValueError("'dual_perspective' is not allowed with 'directed=\"top_to_bottom\"'.")

        # if dual_perspective and directed == "top_to_bottom":
        #     # Y-asymmetrical weight strategies are ambiguous and pose problems for dual-perspective visibility graphs.
        #     # If we assume that the y-direction used to calculate the weights is reflected along with the visibility calculation,
        #     # then one same edge (of contiguous data points) can have two different weight values (e.g. slope can be positive in the original ts and negative in the reflected ts).
        #     # If we assume that the original y-direction is conserved when calculating the weights in the reflected case,
        #     # Therefore, we must use multigraphs, or, more easily, enforce that the weight of an edge must always be the same in the original and in the reflected case.

        #     raise ValueError("'dual_perspective' is not allowed with 'directed=\"top_to_bottom\"'.")

        self.dual_perspective = dual_perspective
        """`bool` indicating whether the visibility graph is dual-perspective visibility graph."""

    def _validate_is_built(self):
        if self._edges is None:
            raise NotBuiltError("Cannot access graph edges, use 'build' first.")

    def build(self, ts, xs=None, only_degrees: bool = False):
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
        if self.dual_perspective and only_degrees:
            raise ValueError("'dual_perspective' is only allowed with 'only_degrees=False'.")

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

        self._edges, self._degrees_in, self._degrees_out = self._compute_graph(self.ts, self.xs, only_degrees)

        if self.dual_perspective:
            # compute vg of reflected ts
            reflect_weight = self.is_weighted and not _WEIGHTED_OPTIONS[self.weighted]["y_symmetric"]

            r_edges, r_degrees_in, r_degrees_out = self._compute_graph(
                -self.ts,
                self.xs,
                only_degrees,
                weight_mult=-1.0 if reflect_weight else 1.0,
                exclude_contiguous=True,
            )

            # note that the only edges that can exist in both the original and the reflected visibility graphs are edges of contiguous nodes.
            # if min_weight and max_weight are not defined, then all contiguous nodes are connected in both the original and reflected VGs.
            # if min_weight or max_weight are defined, then the original and reflected VGs have the same subset of connected contiguous nodes
            # because we are enforcing that an edge cannot have a different weight in the original and contiguous VG (to accomplish this,
            # we multiply by -1.0 the weights in the reflected case if needed).
            # therefore, by excluding edges of contiguous nodes in the reflected visibility graph we have:
            #   - the edge list of the union of the two graphs is just the concatenation of the previous two edge lists.
            #   - the degree sequence of the union of the two graphs is just the addition of the previous two degree sequences.

            self._edges.extend(r_edges)
            self._degrees_in += r_degrees_in
            self._degrees_out += r_degrees_out

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
    def n_vertices(self):
        """
        Number of vertices (nodes) in the graph.
        """
        return self.ts.size

    @property
    def n_edges(self):
        """
        Number of edges (links) in the graph.
        """
        if self._m is None:
            if self._edges is not None:
                self._m = len(self._edges)
            elif self._degrees is not None:
                self._m = np.sum(self._degrees, dtype=int) // 2
            else:
                raise NotBuiltError("Cannot access graph edges, use 'build' first.")

        return self._m

    @property
    def edges(self):
        """
        List of edges of the graph.

        Return the graph edges as an iterable of pairs of integers
        where each integer corresponds to a node id (assigned sequentially in the same order as the input time series).

        If the graph is weighted, a third value is included for each edge corresponding to its weight.
        """
        self._validate_is_built()

        return self._edges

    @property
    def _edges_array(self):
        arr = np.asarray(self._edges, dtype="int64")  # could be 'uint64' but then it breaks np.bincount

        if self.is_weighted:
            return arr[:, :2]

        return arr

    @property
    def weights(self):
        """
        Weights of the edges of the graph.

        Return a 1D array containing the weights of the edges of the graph (listed in the same order as in :attr:`edges`).
        ``None`` if the graph is unweighted.
        """
        self._validate_is_built()

        if self.weighted is None:
            return None

        return np.fromiter((w for (_, _, w) in self.edges), dtype="float64", count=self.n_edges)

    @property
    def degrees(self):
        """
        Degree sequence of the graph.

        Return a list of degree values for each node in the graph, in the same order as the input time series.
        """
        if self._degrees is not None:
            pass
        elif self._edges is not None:
            self._degrees = np.bincount(self._edges_array.flat)
        else:
            raise NotBuiltError("Cannot access graph edges, use 'build' first.")

        return self._degrees

    @property
    def degrees_in(self):
        return self._degrees_in

    @property
    def degrees_out(self):
        return self._degrees_out

    @property
    def degree_counts(self):
        """
        Degree counts of the graph.

        Two lists `ks`, `cs` are returned.
        `cs[i]` is the number of nodes in the graph that have degree `ks[i]`.

        The count of any other degree value not listed in `ks` is 0.
        """
        ks, counts = np.unique(self.degrees, return_counts=True)
        cs = counts

        return ks, cs

    @property
    def degree_distribution(self):
        """
        Degree distribution of the graph.

        Two lists `ks`, `ps` are returned.
        `ps[i]` is the empirical probability that a node in the graph has degree `ks[i]`.

        The probability for any other degree value not listed in `ks` is 0.
        """
        ks, counts = self.degree_counts
        ps = counts / self.n_vertices

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
            The default value used in the matrix for the cases where the nodes are not connected.
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

        e = self._edges_array
        w = self.weights

        if self.is_weighted and use_weights:
            m = np.full((self.n_vertices, self.n_vertices), fill_value=no_weight_value, dtype="float64")
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

        g = Graph.TupleList(self.edges, edge_attrs="weight" if self.is_weighted else None, directed=self.is_directed)

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
            raise ValueError("SNAP weighted graphs not currently supported.")

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

    def summary(self):
        """
        Short text summary describing the graph.

        Returns
        -------
        str
            A string containing the short summary.
        """
        raise NotImplementedError

    # def _compute_graph(self):
    #     raise NotImplementedError()
