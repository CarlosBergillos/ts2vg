.. |ts2vg| replace:: **ts2vg**

.. |cover| image:: https://raw.githubusercontent.com/CarlosBergillos/ts2vg/main/docs/source/images/cover_vg.png
   :width: 100 %
   :alt: Example plot of a visibility graph

.. _Examples: https://carlosbergillos.github.io/ts2vg/examples.html

.. _API Reference: https://carlosbergillos.github.io/ts2vg/api/index.html

.. sphinx-start

|ts2vg|: Time series to visibility graphs
===========================================

|pypi| |pyversions| |wheel| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/ts2vg.svg
   :target: https://pypi.python.org/pypi/ts2vg

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/ts2vg.svg
   :target: https://pypi.python.org/pypi/ts2vg

.. |wheel| image:: https://img.shields.io/pypi/wheel/ts2vg.svg
   :target: https://pypi.python.org/pypi/ts2vg

.. |license| image:: https://img.shields.io/pypi/l/ts2vg.svg
   :target: https://pypi.python.org/pypi/ts2vg

|cover|

|

The Python |ts2vg| package provides high-performance algorithm
implementations to build visibility graphs from time series data.

The visibility graphs and some of their properties (e.g. degree
distributions) are computed quickly and efficiently, even for time
series with millions of observations thanks to the use of `NumPy`_ and
a custom C backend (via `Cython`_) developed for the
visibility algorithms.

The visibility graphs are provided according to the
mathematical definitions described in:

-  Lucas Lacasa et al., "*From time series to complex networks: The visibility graph*", 2008.
-  Lucas Lacasa et al., "*Horizontal visibility graphs: exact results for random time series*", 2009.

An efficient divide-and-conquer algorithm is used to compute the graphs,
as described in:

-  Xin Lan et al., "*Fast transformation from time series to visibility graphs*", 2015.

   
Installation
------------

The latest released |ts2vg| version is available at the `Python Package Index (PyPI)`_
and can be easily installed by running:

.. code:: sh

   pip install ts2vg

For other advanced uses, to build |ts2vg| from source Cython is
required.


Basic usage
-----------

Visibility graph
~~~~~~~~~~~~~~~~

Building the visibility graph for a time series is very simple:

.. code:: python

   from ts2vg import NaturalVG

   ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

   g = NaturalVG()
   g.build(ts)

   edges = g.edges

The time series passed can be a list, a tuple, or a ``numpy`` 1D array.

Horizontal visibility graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also obtain horizontal visibility in a very similar way:

.. code:: python

   from ts2vg import HorizontalVG

   ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

   g = HorizontalVG()
   g.build(ts)

   edges = g.edges

Degree distribution
~~~~~~~~~~~~~~~~~~~

If we are only interested in the degree distribution of the visibility graph
we can pass ``only_degrees=True`` to the ``build`` method.
This will be more efficient in time and memory than computing the whole graph.

.. code:: python

   g = NaturalVG()
   g.build(ts, only_degrees=True)

   ks, ps = g.degree_distribution

Directed visibility graph
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   g = NaturalVG(directed='left_to_right')
   g.build(ts)

Weighted visibility graph
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

   g = NaturalVG(weighted='distance')
   g.build(ts)

|

.. **For more information and options see:** :ref:`Examples` and :ref:`API Reference`.

**For more information and options see:** `Examples`_ and `API Reference`_.


Interoperability with other libraries
-------------------------------------

The graphs obtained can be easily converted to graph objects
from other common Python graph libraries such as `igraph`_, `NetworkX`_ and `SNAP`_
for further analysis.

The following methods are provided:

.. -  :meth:`~ts2vg.graph.base.BaseVG.as_igraph`
.. -  :meth:`~ts2vg.graph.base.BaseVG.as_networkx`
.. -  :meth:`~ts2vg.graph.base.BaseVG.as_snap`

-  ``as_igraph()``
-  ``as_networkx()``
-  ``as_snap()``

For example:

.. code:: python

   g = NaturalVG()
   g.build(ts)
   
   nx_g = g.as_networkx()


Command line interface
----------------------

|ts2vg| can also be used as a command line program directly from the console:

.. code:: sh

   ts2vg ./timeseries.txt -o out.edg 

For more help and a list of options run:

.. code:: sh

   ts2vg --help


Contributing
------------

|ts2vg| can be found `on GitHub`_.
Pull requests and issue reports are welcome.


License
-------

|ts2vg| is licensed under the terms of the `MIT License`_.

.. _NumPy: https://numpy.org/
.. _Cython: https://cython.org/
.. _Python Package Index (PyPI): https://pypi.org/project/ts2vg
.. _igraph: https://igraph.org/python/
.. _NetworkX: https://networkx.github.io/
.. _SNAP: https://snap.stanford.edu/snappy/
.. _on GitHub: https://github.com/CarlosBergillos/ts2vg
.. _MIT License: https://github.com/CarlosBergillos/ts2vg/blob/main/LICENSE
