from ts2vg import NaturalVG, HorizontalVG
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import ArrowStyle, FancyArrowPatch


def plot_graph_demo(
    g, ax, title=None, weights_cmap="coolwarm_r", weights_range=(-3.5, 3.5), cbar_ax=None, arrow_heads="auto"
):
    """
    Draw a simple plot of a time series and its corresponding visibility graph for demonstration purposes.
    Only practical for small graphs (smaller than ~20 nodes).

    Parameters
    ----------
    g : ts2vg.graph.BaseGraph
        Graph object.

    ax : Matplotlib ``Axes``
        Axes where to plot.

    title : str, None
        Plot title. Default ``None``.

    weights_cmap : str, Matplotlib ``Colormap`` object
        Colormap for coloring graph edges based on weight.
        Ignored for unweighted graphs.

    weights_range : tuple
        Range (min, max) used to normalize the coloring of the edge weights.
        Ignored for unweighted graphs.

    cbar_ax : Matplotlib ``Axes`` object
        Axes where to draw the colorbar.
        Ignored for unweighted graphs.

    arrow_heads: 'auto', bool
        Whether to draw arrow heads on the edges.
        If 'auto', will be based on the graph type.
    """
    color_mappable = ScalarMappable(norm=Normalize(*weights_range), cmap=weights_cmap)

    bars = ax.bar(g.xs, g.ts, color="#ccc", edgecolor="#000", width=0.3)
    ax.set_xticks(g.xs)

    if arrow_heads is False or (arrow_heads == "auto" and not g.is_directed):
        arrowstyle = ArrowStyle("-")
    elif g.is_directed:
        arrowstyle = ArrowStyle("-|>", head_length=6, head_width=3)
    else:
        arrowstyle = ArrowStyle("<|-|>", head_length=6, head_width=3)

    if g.is_weighted:
        if cbar_ax is not None:
            cbar_ax.get_figure().colorbar(color_mappable, cax=cbar_ax, orientation="vertical", aspect=30, pad=0.05)
        else:
            ax.get_figure().colorbar(color_mappable, ax=ax, orientation="vertical", aspect=30, pad=0.05)

    for (n1, n2, *w) in g.edges:
        if type(g) == NaturalVG:
            x1, y1 = g.xs[n1], g.ts[n1]
            x2, y2 = g.xs[n2], g.ts[n2]
        elif type(g) == HorizontalVG:
            y = min(g.ts[n1], g.ts[n2])

            if n1 < n2:
                x1, y1 = g.xs[n1] + bars[n1].get_width() / 2, y
                x2, y2 = g.xs[n2] - bars[n2].get_width() / 2, y
            else:
                x1, y1 = g.xs[n1] - bars[n1].get_width() / 2, y
                x2, y2 = g.xs[n2] + bars[n2].get_width() / 2, y
        else:
            raise ValueError(f"Visibility graph type {type(g)} not recognized for plotting.")

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=arrowstyle,
            shrinkA=0,
            shrinkB=0,
            color=color_mappable.to_rgba(*w, alpha=1) if g.is_weighted else (0.25, 0.25, 0.25, 0.7),
            linewidth=2,
        )

        ax.add_patch(arrow)

    if title is not None:
        ax.set_title(title)
