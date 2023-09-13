from typing import Any, Dict, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ts2vg.graph.base import VG


def _simple_title_line(title: str, line_width: int) -> str:
    line = " " * ((line_width - len(title)) // 2)
    line += title
    line += " " * ((line_width - len(title)) // 2)
    line += " " if (len(title) % 2 == 1) else ""
    line += "\n"

    return line


def _simple_key_value_line(key: Any, value: str, line_width: int) -> str:
    key = str(key)

    value = str(value)

    line = key
    line += " " * (line_width - len(key) - len(value))
    line += value
    line += "\n"

    return line


def simple_summary(vg: "VG", title: str = "Visibility Graph", line_width: int = 48) -> str:
    vg._validate_is_built()

    vg_config: Dict[str, Any] = {
        "General Type:": vg._general_type_name,
        "Directed:": vg.directed if vg.is_directed else "undirected",
        "Weighted:": vg.weighted if vg.is_weighted else "unweighted",
        "Parametric Min. Weight:": vg.min_weight if vg.min_weight is not None else "--",
        "Parametric Max. Weight:": vg.max_weight if vg.max_weight is not None else "--",
        "Penetrable Limit:": vg.penetrable_limit,
    }

    built_vg_config: Dict[str, Any] = {
        "Time Series Length:": vg.n_vertices,
        "No. Vertices:": vg.n_vertices,
        "No. Edges:": vg.n_edges,
    }

    txt = _simple_title_line(title, line_width)
    txt += "=" * line_width + "\n"

    for key, value in vg_config.items():
        txt += _simple_key_value_line(key, value, line_width)

    txt += "-" * line_width + "\n"

    for key, value in built_vg_config.items():
        txt += _simple_key_value_line(key, value, line_width)

    txt += "=" * line_width + "\n"

    return txt
