Changelog
=========

**1.2.4** 
---------

*13-07-2024*

Highlights:

+ Added support for NumPy 2.0.
+ Added support for Python 3.12, dropped support for Python 3.6, 3.7 and 3.8.
+ Removed ``setup.cfg`` file in favor of ``pyproject.toml``.


**1.2.3** 
---------

*10-09-2023*

Highlights:

+ Add ``edges_unweighted`` property to graph classes.
+ Fix internal order of nodes in generated *NetworkX* and *igraph* graphs.
  Before this, nodes were added to the *NetworkX* and *igraph* graphs in an unspecified order and this could result in, for example, unsorted and potentially misleading adjacency matrices when using the methods from these libraries.


**1.2.2** 
---------

*10-04-2023*

Highlights:

+ Fixed and refactored CLI application.
+ Switched to C++ for Cython files and now using native C++ queue class.


**1.2.1** 
---------

*10-02-2023*

Highlights:

+ Added new weight option ``"num_penetrations"`` for Limited Penetrable Visibility Graphs.


**1.2.0** 
---------

*06-02-2023*

Highlights:

+ Added Limited Penetrable Visibility Graphs (via the ``penetrable_limit`` parameter).
+ Renamed base class ``BaseVG`` to ``VG``.


**1.1.1** 
---------

*23-01-2023*

Highlights:

+ Added tolerance to Natural Visibility Graph slope comparisons to mitigate floating point errors.


**1.1.0** 
---------

*21-01-2023*

Highlights:

+ Added Parametric Visibility Graph capabilities via ``min_weight`` and ``max_weight``.
+ General clean-up and refactor of some parts of the code.


**1.0.0** 
---------

*20-08-2021*

Major project overhaul.
Some of the highlights are:

+ Cleaned and improved code base
+ Added horizontal visibility graphs
+ Added directed graphs
+ Added weighted graphs
+ Added automated tests using *pytest*
+ New project documentation using *Sphinx*


**0.1**
-------

*20-06-2020*

Initial release.
