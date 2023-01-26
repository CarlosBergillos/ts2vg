from ts2vg import NaturalVG

ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

g = NaturalVG().build(ts)

g.adjacency_matrix(triangle="lower")
