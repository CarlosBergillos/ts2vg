from plot_graph_demo import plot_graph_demo

# ~~
from ts2vg import NaturalVG
import matplotlib.pyplot as plt

ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

weight_options = [
    "slope",
    "abs_slope",
    "distance",
    "h_distance",
    "v_distance",
    "abs_v_distance",
]

fig, axs = plt.subplots(ncols=3, nrows=2, figsize=(12, 6))
cbar_ax = fig.add_axes([0.96, 0.2, 0.01, 0.6])

for w, ax in zip(weight_options, axs.flat):
    g = NaturalVG(weighted=w).build(ts)
    plot_graph_demo(g, ax=ax, title=f"weighted='{w}'", cbar_ax=cbar_ax)
