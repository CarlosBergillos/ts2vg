from plot_utils import plot_graph_demo, plot_horizontal_graph_demo

# ~~
from ts2vg import NaturalVG, HorizontalVG
import matplotlib.pyplot as plt


ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

nvg_default = NaturalVG().build(ts)
hvg_default = HorizontalVG().build(ts)

penetrable_limit_options = [
    0,
    1,
    2,
]

fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(12, 7))

# plot limited penetrable visibility graphs
for penetrable_limit, ax in zip(penetrable_limit_options, axs.flat[:3]):
    ax.set_title(f"NVG, penetrable_limit={penetrable_limit}")

    nvg = NaturalVG(penetrable_limit=penetrable_limit).build(ts)
    added_edges = set(nvg.edges) - set(nvg_default.edges)

    plot_graph_demo(nvg, marked_edges=added_edges, ax=ax)

# plot limited penetrable horizontal visibility graphs
for penetrable_limit, ax in zip(penetrable_limit_options, axs.flat[3:]):
    ax.set_title(f"HVG, penetrable_limit={penetrable_limit}")

    hvg = HorizontalVG(penetrable_limit=penetrable_limit).build(ts)
    added_edges = set(hvg.edges) - set(hvg_default.edges)

    plot_horizontal_graph_demo(hvg, marked_edges=added_edges, ax=ax)
