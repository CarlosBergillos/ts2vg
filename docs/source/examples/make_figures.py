from pathlib import Path

basic_filepath = Path("basic.png")
degree_distribution_filepath = Path("degree_distribution.svg")
directed_filepath = Path("directed.svg")
weighted_filepath = Path("weighted.svg")
horizontal_filepath = Path("horizontal.svg")
partitioning_filepath = Path("partitioning.png")

if not basic_filepath.exists():
    from basic import ax1, ax2, fig

    ax1.margins(x=0, y=0)
    ax2.margins(x=0, y=0)
    fig.tight_layout(w_pad=3)
    fig.savefig(basic_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")


if not degree_distribution_filepath.exists():
    from degree_distribution import fig

    fig.tight_layout(w_pad=2)
    fig.savefig(degree_distribution_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")


if not directed_filepath.exists():
    from directed import fig

    fig.tight_layout(w_pad=2)
    fig.savefig(directed_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")


if not weighted_filepath.exists():
    from weighted import fig

    fig.tight_layout(w_pad=2)
    fig.subplots_adjust(right=0.94)
    fig.savefig(weighted_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")


if not horizontal_filepath.exists():
    from horizontal import fig

    fig.tight_layout(w_pad=2)
    fig.savefig(horizontal_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")


if not partitioning_filepath.exists():
    from partitioning import ax1, ax2, fig

    ax1.margins(x=0, y=0)
    ax2.margins(x=0, y=0)
    fig.tight_layout(w_pad=3)
    fig.savefig(partitioning_filepath, facecolor=(0, 0, 0, 0), bbox_inches="tight")
