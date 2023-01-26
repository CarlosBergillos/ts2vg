Examples
========

Computing and drawing visibility graphs
---------------------------------------

This example builds the visibility graph for a randomly generated motion time series
and draws the graph with the help of `NetworkX <https://networkx.github.io/>`_.

.. literalinclude:: examples/basic.py
    :language: python


.. figure:: examples/basic.png
   :width: 100%
   :alt: Example plots of a visibility graph


Obtaining the adjacency matrix
------------------------------

This example shows how to obtain the adjacency matrix for the visibility graph of a time series.

See :meth:`adjacency_matrix() <ts2vg.NaturalVG.adjacency_matrix>` for more options.


.. literalinclude:: examples/adjacency_matrix.py
    :language: python


::

    array([[0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 0, 0, 0, 0, 0],
       [1, 1, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 1, 1, 0, 0],
       [0, 0, 0, 0, 1, 1, 1, 0]], dtype=uint8)


Obtaining the degree distribution
---------------------------------

This example shows how to get the degree distribution for the visibility graph of a given time series.

Here, we generate a random time series with 100.000 data points and then compute and plot its degree distribution.


.. literalinclude:: examples/degree_distribution.py
    :language: python


.. figure:: examples/degree_distribution.svg
    :width: 100%
    :alt: Example degree distribution


Building directed graphs
------------------------

This example illustrates different options for the ``directed`` parameter when building visibility graphs.


.. literalinclude:: examples/directed.py
    :language: python
    :start-after: # ~~


.. figure:: examples/directed.svg
   :width: 100%
   :alt: Example directed graphs


.. admonition:: Code for :meth:`plot_graph_demo`
   :class: toggle

    .. literalinclude:: examples/plot_graph_demo.py
        :language: python


Building weighted graphs
------------------------

This example illustrates different options for the ``weighted`` parameter when building visibility graphs.

.. literalinclude:: examples/weighted.py
    :language: python
    :start-after: # ~~


.. figure:: examples/weighted.svg
   :width: 100%
   :alt: Example weighted graphs


.. admonition:: Code for :meth:`plot_graph_demo`
   :class: toggle

    .. literalinclude:: examples/plot_graph_demo.py
        :language: python


Building horizontal visibility graphs
-------------------------------------

This example illustrates different options for horizontal visibility graphs.
Note that horizontal visibility graphs can also be directed and/or weighted.

.. literalinclude:: examples/horizontal.py
    :language: python
    :start-after: # ~~


.. figure:: examples/horizontal.svg
   :width: 100%
   :alt: Example horizontal visibility graphs


.. admonition:: Code for :meth:`plot_graph_demo`
   :class: toggle

    .. literalinclude:: examples/plot_graph_demo.py
        :language: python


Partitioning time series via community detection
------------------------------------------------

Time series can be partitioned by applying community detection algorithms to their visibility graphs.

.. literalinclude:: examples/partitioning.py
    :language: python


.. figure:: examples/partitioning.png
   :width: 100%
   :alt: Example partitioning of visibility graphs


.. admonition:: Code for :meth:`plot_graph_demo`
   :class: toggle

    .. literalinclude:: examples/plot_graph_demo.py
        :language: python
