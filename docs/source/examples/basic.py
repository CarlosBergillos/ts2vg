from ts2vg import NaturalVG
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# 1. Generate random time series (Brownian motion)
rng = np.random.default_rng(110)
ts = rng.standard_normal(size=200)
ts = np.cumsum(ts)

# 2. Build visibility graph
g = NaturalVG(directed=None).build(ts)
nxg = g.as_networkx()

# 3. Make plots
fig, [ax0, ax1, ax2] = plt.subplots(ncols=3, figsize=(12, 3.5))

ax0.plot(ts)
ax0.set_title("Time Series")

graph_plot_options = {
    "with_labels": False,
    "node_size": 2,
    "node_color": [(0, 0, 0, 1)],
    "edge_color": [(0, 0, 0, 0.15)],
}

nx.draw_networkx(nxg, ax=ax1, pos=g.node_positions(), **graph_plot_options)
ax1.tick_params(bottom=True, labelbottom=True)
ax1.plot(ts)
ax1.set_title("Visibility Graph")

nx.draw_networkx(nxg, ax=ax2, pos=nx.kamada_kawai_layout(nxg), **graph_plot_options)
ax2.set_title("Visibility Graph")
