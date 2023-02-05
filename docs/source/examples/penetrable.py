from plot_utils import plot_graph_demo

# ~~
from ts2vg import NaturalVG
import matplotlib.pyplot as plt


ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

penetrable_limit_options = [
    0,
    1,
    2,
]

fig, axs = plt.subplots(ncols=3, figsize=(12, 3.5))

for penetrable_limit, ax in zip(penetrable_limit_options, axs):
    ax.set_title(f"penetrable_limit={penetrable_limit}")

    # plot the complete penetrable graph in red
    g = NaturalVG(penetrable_limit=penetrable_limit).build(ts)
    plot_graph_demo(g, ax=ax, edge_color="#FF8080")

    # plot the default non-penetrable graph in gray on top
    g_default = NaturalVG().build(ts)
    plot_graph_demo(g_default, ax=ax, edge_color="#808080", plot_bars=False)
