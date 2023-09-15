import argparse
from typing import Dict, List
from pathlib import Path

import numpy as np

from ts2vg import NaturalVG, HorizontalVG
from ts2vg.graph.base import _DIRECTED_OPTIONS, _WEIGHTED_OPTIONS

_OUTPUT_MODES: Dict[str, str] = {
    "el": "edge list",
    "ds": "degree sequence",
    "dd": "degree distribution",
    "dc": "degree counts",
}

_GRAPH_TYPES: Dict[str, VG] = {
    "natural": NaturalVG,
    "horizontal": HorizontalVG,
}


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text: str, width: int) -> List[str]:
        if text.startswith("R|"):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts: List[str] = []

            if action.nargs == 0:
                parts.extend(action.option_strings)

            else:
                default = self._get_default_metavar_for_optional(action)
                for option_string in action.option_strings:
                    parts.append(option_string)
                parts.append(default)

            return " ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        formatter_class=SmartFormatter,
        description="Compute the visibility graph from an input time series.",
    )

    parser.add_argument(
        "input",
        help="Path to the file containing the input time series. Must be a text file with one value per line.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Path to the file where the output corresponding to the visibility graph will be saved. If not provided, output will go to stdout.",
    )

    graph_type_options = _GRAPH_TYPES.keys()
    parser.add_argument(
        "-t",
        "--type",
        choices=graph_type_options,
        default="natural",
        help="General type of graph. {" + ",".join(graph_type_options) + "}",
    )

    directed_choices = [c for c in _DIRECTED_OPTIONS.keys() if c is not None]
    parser.add_argument(
        "-d",
        "--directed",
        choices=directed_choices,
        default=None,
        help="If provided, build a directed graph with one of the following values: {"
        + ",".join(directed_choices)
        + "}.",
    )

    weighted_choices = [c for c in _WEIGHTED_OPTIONS.keys() if c is not None]
    parser.add_argument(
        "-w",
        "--weighted",
        choices=weighted_choices,
        default=None,
        help="If provided, build a weighted graph with one of the following values: {"
        + ",".join(weighted_choices)
        + "}.",
    )

    parser.add_argument(
        "-p",
        "--penetrable_limit",
        type=int,
        default=0,
        help="If larger than 0, build a limited penetrable visibility graph (LPVG) with this number of maximum allowed penetrations per edge.",
    )

    parser.add_argument(
        "-m",
        "--outputmode",
        choices=_OUTPUT_MODES.keys(),
        default="el",  # metavar="",
        help="R|Graph properties and representation to use for the output. One of:"
        "\n el : (default) Edge list. Nodes are labelled in the range [0, n-1] in the same order as the input time series."
        "\n ds :           Degree sequence. Degree values for the nodes in the range [0, n-1] in the same order as the input time series."
        "\n dd :           Degree distribution. 1st column is a degree value (k) and 2nd column is the empirical probability for that degree k."
        "\n dc :           Degree counts. 1st column is a degree value (k) and 2nd column is the number of nodes with that degree k.",
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    gtype = args.type
    directed = args.directed
    weighted = args.weighted
    penetrable_limit = args.penetrable_limit
    output_mode = args.outputmode

    output_f = None
    if output_path is not None:
        output_path_ = Path(output_path)
        if not output_path_.parent.exists():
            print(f"ERROR: Output folder for '{output_path}' not found.")
            return 1

        output_f = open(output_path, "w")

    input_path_ = Path(input_path)
    if not input_path_.is_file():
        print(f"ERROR: Input file '{input_path}' not found.")
        return 1

    build_only_degrees = output_mode in ["ds", "dd", "dc"]

    ts = np.loadtxt(input_path_, dtype="float64")

    g = _GRAPH_TYPES[gtype](directed=directed, weighted=weighted, penetrable_limit=penetrable_limit)
    g.build(ts, only_degrees=build_only_degrees)

    if output_mode == "el":
        es = g.edges
        for (a, b, *w) in es:
            print(a, b, *w, file=output_f)
    elif output_mode == "ds":
        ds = g.degrees
        for d in ds:
            print(d, file=output_f)
    elif output_mode == "dd":
        ks, pks = g.degree_distribution
        for k, pk in zip(ks, pks):
            print(k, pk, file=output_f)
    elif output_mode == "dc":
        ks, nks = g.degree_counts
        for k, nk in zip(ks, nks):
            print(k, nk, file=output_f)

    if output_path is not None:
        output_f.close()
        print(g.summary())
        print(f"Saved {_OUTPUT_MODES[output_mode]} to file: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
