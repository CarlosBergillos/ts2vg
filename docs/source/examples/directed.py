from plot_graph_demo import plot_graph_demo

# ~~
from ts2vg import NaturalVG
import matplotlib.pyplot as plt

ts = [6.0, 3.0, 1.8, 4.2, 6.0, 3.0, 1.8, 4.8]

direction_options = [
    None,
    "left_to_right",
    "top_to_bottom",
]

fig, axs = plt.subplots(ncols=3, figsize=(12, 3.5))

for d, ax in zip(direction_options, axs.flat):
    g = NaturalVG(directed=d).build(ts)
    plot_graph_demo(g, ax=ax, title=f"directed={repr(d)}")
