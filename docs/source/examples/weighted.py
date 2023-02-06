from plot_utils import plot_weighted_nvg

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
    ax.set_title(f"weighted='{w}'")

    nvg = NaturalVG(weighted=w).build(ts)
    plot_weighted_nvg(nvg, ax=ax, cbar_ax=cbar_ax)
