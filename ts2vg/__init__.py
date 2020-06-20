"""
<div align="center">
    <img alt="Example of a Visibility Graph Visualized" src="example_vg.png" style="width: 100%; max-width: 650px;" >
</div>

The Python `ts2vg` package provides high-performance algorithm implementations to obtain visibility graphs from time series data. 

The visibility graphs and some of their properties (e.g. degree distributions) are computed quickly and efficiently, even for time series with millions of observations, thanks to the use of [NumPy](https://numpy.org/) and a custom C backend (with the help of [Cython](https://cython.org/)) developed for the visibility algorithms.

The (natural) visibility graphs are provided according to the mathematical definitions described in:

* Lucas Lacasa et al., "From time series to complex networks: The visibility graph", 2008.

An efficient divide-and-conquer algorithm is used, as described in:

* Xin Lan et al., "Fast transformation from time series to visibility graphs", 2015

## Installation
The latest released `ts2vg` version is available at the [Python
Package Index](https://pypi.org/project/ts2vg) and can be easily installed by running:
```sh
pip install ts2vg
```

For other advanced uses, to install `ts2vg` from source, Cython is required.

## Python basic usage
Obtaining the edge list for the visibility graph of a time series:
```python
from ts2vg import NaturalVisibilityGraph

ts = [0.87, 0.48, 0.36, 0.83, 0.87, 0.48, 0.36, 0.83]
edges = NaturalVisibilityGraph(ts).edgelist()
```

Obtaining the degree distribution for the visibility graph of a time series:
```python
from ts2vg import NaturalVisibilityGraph

ts = [0.87, 0.48, 0.36, 0.83, 0.87, 0.48, 0.36, 0.83]
ks, pks = NaturalVisibilityGraph(ts).degree_distribution()
```

To obtain an [igraph](https://igraph.org/python/), [NetworkX](https://networkx.github.io/) or [SNAP](https://snap.stanford.edu/snappy/) graph object the following methods are provided:

* `as_igraph()` 
* `as_networkx()` 
* `as_snap()` 

```python
from ts2vg import NaturalVisibilityGraph

ts = [0.87, 0.48, 0.36, 0.83, 0.87, 0.48, 0.36, 0.83]
vg = NaturalVisibilityGraph(ts).as_igraph()
```
For full documentation visit **

## Command Line Interface
`ts2vg` can also be used as a command line program directly from the console:
```sh
ts2vg ./timeseries.txt -o out.edg 
```
Use `ts2vg -h` to see additional help on the command line program use and features.

Contributing
------------
`ts2vg` can be found [on GitHub](https://github.com/CarlosBergillos/ts2vg)

License
-------
`ts2vg` is licensed under the terms of the [MIT License](https://github.com/CarlosBergillos/ts2vg/blob/master/LICENSE).
"""

__pdoc__ = {}
__pdoc__['ts2vg.cli'] = False
__pdoc__['ts2vg.nvg'] = False
__pdoc__['ts2vg.pairqueue'] = False

import numpy as np
from ts2vg.nvg import nvg_edges, nvg_degrees


__all__ = [
    'VisibilityGraphBase',
    'NaturalVisibilityGraph'
]


class VisibilityGraphBase:
    """
    Abstract class. Should not be instantiated directly, but through its subclasses instead, e.g with `NaturalVisibilityGraph`.

    Args:
        ts (list of values, or 1d numpy array): Time series data to use as input for the visibility graph.
    """
    def __init__(self, ts, *args):
        """
        .. note::
            The visibility graph or its properties might not be computed at initialization but until some method or attribute that requires it is called for the first time.
        """
        if type(self) is VisibilityGraphBase:
            raise NotImplementedError("Use one of the subclasses: e.g NaturalVisibilityGraph")

        self.ts = np.asarray(ts, dtype=np.float64)
        if self.ts.ndim != 1:
            raise ValueError("Input data must be one-dimensional")
        
        self._m = None
        self._edgelist = None
        self._degree_sequence = None
        #self._degree_distribution = None

    #@property
    def number_of_vertices(self):
        """
        Number of vertices (nodes) in the graph.
        """
        return self.ts.size
    
    #@property
    def number_of_edges(self):
        """
        Number of edges (links) in the graph.
        """
        if self._m is None:
            if self._edgelist is not None:
                self._m = len(self._edgelist)
            else:
                self._m = np.sum(self.degree_sequence(), dtype=int) // 2
            
        return self._m
    
    #@property
    def edgelist(self):
        """
        List of edges of the graph. Each edge is represented via a pair of ints corresponding to the node labels.
        """
        if self._edgelist is None:
            self._edgelist = self._obtain_edges()
        
        return self._edgelist
    
    #@property
    def degree_sequence(self):
        """
        Degree sequence of the graph. Degree values for all the nodes in the graph and listed in the time series order [0, n-1].
        """
        if self._degree_sequence is None:
            self._degree_sequence = self._obtain_degree_sequence()
        
        return self._degree_sequence
    
    #@property
    def degree_counts(self):
        """
        Degree counts of the graph.
        Two lists `k`, `ck` are returned.
        `ck[i]` counts the number of nodes in the graph that have degree `k[i]`.
        The count of any other degree value not listed in `k` is 0.
        """
        ks, counts = np.unique(self.degree_sequence(), return_counts=True)
        return ks, counts
    
    #@property
    def degree_distribution(self):
        """
        Degree distribution of the graph.
        Two lists `k`, `pk` are returned.
        `pk[i]` is the empirical probability that a node in the graph has degree `k[i]`.
        The probability for any other degree value not listed in `k` is 0.
        """
        ks, counts = self.degree_counts()
        return ks, counts/self.number_of_vertices()
    
    def as_igraph(self):
        """
        [_igraph_](https://igraph.org/python/) graph object for this graph.
        The `igraph` package must be installed and accessible.
        """
        from igraph import Graph
        
        g = Graph()
        g.add_vertices(self.number_of_vertices())
        g.add_edges(self.edgelist())

        return g
    
    def as_networkx(self):
        """
        [_NetworkX_](https://networkx.github.io/) graph object corresponding to this graph.
        The `networkx` package must be installed and accessible.
        """
        from networkx import Graph
        
        g = Graph()
        g.add_edges_from(self.edgelist())

        return g
    
    def as_snap(self):
        """
        [_SNAP_](https://snap.stanford.edu/snappy/) graph object corresponding to this graph.
        The `snap` package must be installed and accessible.
        """
        from snap import TUNGraph as Graph
        
        g = Graph.New()
        for i in range(self.number_of_vertices()):
            g.AddNode(i)
        for e in self.edgelist():
            g.AddEdge(*e)

        return g


class NaturalVisibilityGraph(VisibilityGraphBase):
    '''
    Representation of a (natural) visibility graph as obtained from an input time series according
    to the mathematical definitions described in:
    
    * Lucas Lacasa et al., "From time series to complex networks: The visibility graph", 2008.
    
    See `VisibilityGraphBase` for the available arguments, methods and attributes.
    '''
    def _obtain_edges(self):
        return nvg_edges(self.ts)
    
    def _obtain_degree_sequence(self):
        return nvg_degrees(self.ts)
