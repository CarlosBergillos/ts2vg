from ts2vg import NaturalVG
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# 1. Generate Brownian motion series
rng = np.random.default_rng(110)
ts = rng.standard_normal(size=200)
ts = np.cumsum(ts)

# 2. Build visibility graph
g = NaturalVG(directed=None).build(ts)
nxg = g.as_networkx()

# 3. Partition the graph into communities
communities = nx.algorithms.community.greedy_modularity_communities(nxg)

# 4. Make plots

COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]

node_colors = ["#000000"] * len(ts)
for community_id, community_nodes in enumerate(communities):
    for node in community_nodes:
        node_colors[node] = COLORS[community_id % len(COLORS)]

fig, [ax0, ax1, ax2] = plt.subplots(ncols=3, figsize=(12, 3.5))

ax0.plot(ts)
ax0.set_title("Time Series")

graph_plot_options = {
    "with_labels": False,
    "node_size": 6,
    "node_color": [node_colors[n] for n in nxg.nodes],
}

nx.draw_networkx(nxg, ax=ax1, pos=g.node_positions(), edge_color=[(0, 0, 0, 0.05)], **graph_plot_options)
ax1.tick_params(bottom=True, labelbottom=True)
ax1.plot(ts, c=(0, 0, 0, 0.15))
ax1.set_title("Visibility Graph")

nx.draw_networkx(nxg, ax=ax2, pos=nx.kamada_kawai_layout(nxg), edge_color=[(0, 0, 0, 0.15)], **graph_plot_options)
ax2.set_title("Visibility Graph")
