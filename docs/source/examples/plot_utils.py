# ~~ plot_nvg
from matplotlib.patches import ArrowStyle, FancyArrowPatch


def plot_nvg(
    vg,
    ax,
    edge_color=(0.25, 0.25, 0.25, 0.7),
):
    bars = ax.bar(vg.xs, vg.ts, color="#ccc", edgecolor="#000", width=0.3)
    ax.set_xticks(vg.xs)

    for (n1, n2) in vg.edges:
        x1, y1 = vg.xs[n1], vg.ts[n1]
        x2, y2 = vg.xs[n2], vg.ts[n2]

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=ArrowStyle("->", head_length=6, head_width=2.5) if vg.is_directed else ArrowStyle("-"),
            shrinkA=0,
            shrinkB=0,
            color=edge_color,
            linewidth=2,
        )

        ax.add_patch(arrow)


# $$

# ~~ plot_hvg
from matplotlib.patches import ArrowStyle, FancyArrowPatch


def plot_hvg(
    vg,
    ax,
    edge_color=(0.25, 0.25, 0.25, 0.7),
    bar_width=0.3,
    prevent_overlap=False,
):
    occupied_heights = set()

    bars = ax.bar(vg.xs, vg.ts, color="#ccc", edgecolor="#000", width=bar_width)
    ax.set_xticks(vg.xs)

    for i, (n1, n2) in enumerate(vg.edges):
        y = min(vg.ts[n1], vg.ts[n2])

        if prevent_overlap:
            # very naive overlap prevention
            while round(y, 2) in occupied_heights:
                y -= 0.18

            occupied_heights.add(round(y, 2))

        if n1 < n2:
            x1, y1 = vg.xs[n1] + (bar_width / 2), y
            x2, y2 = vg.xs[n2] - (bar_width / 2), y
        else:
            x1, y1 = vg.xs[n1] - (bar_width / 2), y
            x2, y2 = vg.xs[n2] + (bar_width / 2), y

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=(
                ArrowStyle("->", head_length=6, head_width=2.5)
                if vg.is_directed
                else ArrowStyle("<->", head_length=6, head_width=2.5)
            ),
            shrinkA=0,
            shrinkB=0,
            color=edge_color,
            linewidth=2,
        )

        ax.add_patch(arrow)


# $$

# ~~ plot_weighted_nvg
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import ArrowStyle, FancyArrowPatch


def plot_weighted_nvg(
    vg,
    ax,
    cbar_ax,
    weights_cmap="coolwarm_r",
    weights_range=(-3.5, 3.5),
):
    bars = ax.bar(vg.xs, vg.ts, color="#ccc", edgecolor="#000", width=0.3)
    ax.set_xticks(vg.xs)

    color_mappable = ScalarMappable(norm=Normalize(*weights_range), cmap=weights_cmap)
    cbar_ax.get_figure().colorbar(color_mappable, cax=cbar_ax, orientation="vertical", aspect=30, pad=0.05)

    for (n1, n2, w) in vg.edges:
        x1, y1 = vg.xs[n1], vg.ts[n1]
        x2, y2 = vg.xs[n2], vg.ts[n2]

        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=ArrowStyle("-"),
            shrinkA=0,
            shrinkB=0,
            color=color_mappable.to_rgba(w, alpha=1),
            linewidth=2,
        )

        ax.add_patch(arrow)


# $$
