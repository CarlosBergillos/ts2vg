from plot_utils import plot_graph_demo

# ~~
from ts2vg import NaturalVG
import matplotlib.pyplot as plt


ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

vg_default = NaturalVG().build(ts)

penetrable_limit_options = [
    0,
    1,
    2,
]

fig, axs = plt.subplots(ncols=3, figsize=(12, 3.5))

for penetrable_limit, ax in zip(penetrable_limit_options, axs):
    ax.set_title(f"penetrable_limit={penetrable_limit}")

    vg = NaturalVG(penetrable_limit=penetrable_limit).build(ts)
    added_edges = set(vg.edges) - set(vg_default.edges)

    plot_graph_demo(vg, marked_edges=added_edges, ax=ax)
