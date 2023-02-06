def _simple_title_line(title, line_width):
    line = " " * ((line_width - len(title)) // 2)
    line += title
    line += " " * ((line_width - len(title)) // 2)
    line += " " if (len(title) % 2 == 1) else ""
    line += "\n"

    return line


def _simple_key_value_line(key, value, line_width):
    key = str(key)

    value = str(value)

    line = key
    line += " " * (line_width - len(key) - len(value))
    line += value
    line += "\n"

    return line


def simple_summary(vg: "ts2vg.graph.base.VG", title: str = "Visibility Graph", line_width: int = 48):
    vg_config = {
        "General Type:": vg.general_type_name,
        "Directed:": vg.directed if vg.is_directed else "undirected",
        "Weighted:": vg.weighted if vg.is_weighted else "unweighted",
        "Parametric Min. Weight:": vg.min_weight if vg.min_weight is not None else "--",
        "Parametric Max. Weight:": vg.max_weight if vg.max_weight is not None else "--",
        "Penetrable Limit:": vg.penetrable_limit,
    }

    built_vg_config = {
        "Time Series Length:": len(vg.ts),
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
