# **ts2vg**

<div align="center">
    <img alt="Example of a Visibility Graph Visualized" src="./docs/example_vg.png" width="650px">
</div>
<!-- ![Example of a Visibility Graph Visualized](/example_vg.png "Visibility Graph Visualized") -->

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

Full documentation and information on all available features be found [**here**](http://carlosbergillos.github.io/ts2vg).

## Command Line Interface
`ts2vg` can also be used as a command line program directly from the console:
```sh
ts2vg ./timeseries.txt -o out.edg 
```
Use `ts2vg -h` to see additional help on the command line program use and features.

## License
`ts2vg` is licensed under the terms of the [MIT License](./LICENSE).

