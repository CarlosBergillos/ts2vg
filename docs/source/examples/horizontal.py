from plot_utils import plot_hvg

# ~~
from ts2vg import HorizontalVG
import matplotlib.pyplot as plt

ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

direction_options = [
    None,
    "left_to_right",
    "top_to_bottom",
]

fig, axs = plt.subplots(ncols=3, figsize=(12, 3.5))

for d, ax in zip(direction_options, axs):
    ax.set_title(f"directed={repr(d)}")

    hvg = HorizontalVG(directed=d).build(ts)
    plot_hvg(hvg, ax=ax)
