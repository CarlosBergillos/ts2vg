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
implementations to build visibility graphs from time series data,
as first introduced by Lucas Lacasa et al. in 2008 [#Lacasa2008]_.

The visibility graphs and some of their properties (e.g. degree
distributions) are computed quickly and efficiently even for time
series with millions of observations.
An efficient divide-and-conquer algorithm is used to compute the graphs
whenever possible [#Lan2015]_.

   
Installation
------------

The latest released |ts2vg| version is available at the `Python Package Index (PyPI)`_
and can be easily installed by running:

.. code:: sh

   pip install ts2vg

For other advanced uses, to build |ts2vg| from source Cython is required.


Supported graph types
---------------------

Root graph types
~~~~~~~~~~~~~~~~

- Natural Visibility Graphs (NVG) [#Lacasa2008]_ (``ts2vg.NaturalVG``)
- Horizontal Visibility Graphs (HVG) [#Lacasa2009]_ (``ts2vg.HorizontalVG``)

Available variations
~~~~~~~~~~~~~~~~~~~~

- Weighted Visibility Graphs (via the ``weighted`` parameter)
- Directed Visibility Graphs (via the ``directed`` parameter)
- Parametric Visibility Graphs [#Bezsudnov2014]_ (via the ``min_weight`` and ``max_weight`` parameters)
- Limited Penetrable Visibility Graphs (LPVG) [#Zhou2012]_ [#Xuan2021]_ (via the ``penetrable_limit`` parameter)

.. - Dual Perspective Visibility Graph [*planned, not implemented yet*]

Note that multiple graph variations can be combined and used simultaneously.


Documentation
-------------

Usage and reference documentation for |ts2vg| can be found at `carlosbergillos.github.io/ts2vg`_.


Basic usage
-----------

To build a visibility graph from a time series do:

.. code:: python

   from ts2vg import NaturalVG

   ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

   vg = NaturalVG()
   vg.build(ts)

   edges = vg.edges


The time series passed (``ts``) can be any one-dimensional iterable, such as a list or a ``numpy`` 1D array.

By default, the input observations are assumed to be equally spaced in time.
Alternatively, a second 1D iterable (``xs``) can be provided for unevenly spaced time series.


Horizontal visibility graphs can be obtained in a very similar way:

.. code:: python

   from ts2vg import HorizontalVG

   ts = [1.0, 0.5, 0.3, 0.7, 1.0, 0.5, 0.3, 0.8]

   vg = HorizontalVG()
   vg.build(ts)

   edges = vg.edges


If we are only interested in the degree distribution of the visibility graph
we can pass ``only_degrees=True`` to the ``build`` method.
This will be more efficient in time and memory than storing the whole graph.

.. code:: python

   vg = NaturalVG()
   vg.build(ts, only_degrees=True)

   ks, ps = vg.degree_distribution


Directed graphs can be obtained by using the ``directed`` parameter
and weighted graphs can be obtained by using the ``weighted`` parameter:

.. code:: python

   vg1 = NaturalVG(directed="left_to_right")
   vg1.build(ts)

   vg2 = NaturalVG(weighted="distance")
   vg2.build(ts)

   vg3 = NaturalVG(directed="left_to_right", weighted="distance")
   vg3.build(ts)

   vg4 = HorizontalVG(directed="left_to_right", weighted="h_distance")
   vg4.build(ts)


.. **For more information and options see:** :ref:`Examples` and :ref:`API Reference`.

For more information and options see: `Examples`_ and `API Reference`_.


Interoperability with other libraries
-------------------------------------

The graphs obtained can be easily converted to graph objects
from other common Python graph libraries such as `igraph`_, `NetworkX`_ and `SNAP`_
for further analysis.

The following methods are provided:

.. -  :meth:`~ts2vg.graph.base.VG.as_igraph`
.. -  :meth:`~ts2vg.graph.base.VG.as_networkx`
.. -  :meth:`~ts2vg.graph.base.VG.as_snap`

-  ``as_igraph()``
-  ``as_networkx()``
-  ``as_snap()``

For example:

.. code:: python

   vg = NaturalVG()
   vg.build(ts)
   
   g = vg.as_networkx()


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
.. _carlosbergillos.github.io/ts2vg: https://carlosbergillos.github.io/ts2vg/


References
----------

.. [#Lacasa2008] Lucas Lacasa et al., "*From time series to complex networks: The visibility graph*", 2008.
.. [#Lacasa2009] Lucas Lacasa et al., "*Horizontal visibility graphs: exact results for random time series*", 2009.
.. [#Lan2015] Xin Lan et al., "*Fast transformation from time series to visibility graphs*", 2015.
.. [#Zhou2012] T.T Zhou et al., "*Limited penetrable visibility graph for establishing complex network from time series*", 2012.
.. [#Bezsudnov2014] I.V. Bezsudnov et al., "*From the time series to the complex networks: The parametric natural visibility graph*", 2014
.. [#Xuan2021] Qi Xuan et al., "*CLPVG: Circular limited penetrable visibility graph as a new network model for time series*", 2021
