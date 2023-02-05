# ~~ plot_graph_demo
from matplotlib.patches import ArrowStyle, FancyArrowPatch


def plot_graph_demo(
    vg,
    ax,
    edge_color=(0.25, 0.25, 0.25, 0.7),
    plot_bars=True,
):

    if plot_bars:
        bars = ax.bar(vg.xs, vg.ts, color="#ccc", edgecolor="#000", width=0.3)
        ax.set_xticks(vg.xs)

    for (n1, n2) in vg.edges:
        x1, y1 = vg.xs[n1], vg.ts[n1]
        x2, y2 = vg.xs[n2], vg.ts[n2]

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=ArrowStyle("-"),
            shrinkA=0,
            shrinkB=0,
            color=edge_color,
            linewidth=2,
        )

        ax.add_patch(arrow)


# $$
