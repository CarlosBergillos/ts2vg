import sys
import argparse
import numpy as np
from pathlib import Path
from ts2vg import NaturalVisibilityGraph

class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        return argparse.HelpFormatter._split_lines(self, text, width)

output_modes = {
    'el': 'edge list',
    'ds': 'degree sequence',
    'dd': 'degree distribution',
    'dc': 'degree counts'
}

def main():
    parser = argparse.ArgumentParser(formatter_class=SmartFormatter, description="Compute the visibility graph from an input time series.")
    parser.add_argument('input', help="Path to the file containing the input time series.")
    parser.add_argument('-o', '--output', help="Path to the file where the output corresponding to the visibility graph will be saved.")
    parser.add_argument('-m', '--outputmode', choices=output_modes.keys(), default='el', #metavar="", 
                        help="R|Graph properties and representation to use for the output. One of:"
                            "\n  el (default) \tEdge list. Nodes are labelled in the range [0, n-1] corresponding to the order in the input time series."
                            "\n  ds \t\tDegree sequence. Degree values for the nodes in the range [0, n-1] in the same order as the input time series."
                            "\n  dd \t\tDegree distribution. 1st column is a degree value (k), and 2nd column is the empirical probability for that degree k."
                            "\n  dc \t\tDegree counts. Like the degree distribution, but not normalized. 1st column is a degree value (k), and 2nd column is the number of nodes with that degree k.")
    #todo -dc
    
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    output_mode = args.outputmode
    
    f_output = None
    if output_path is not None:
        f_output = open(output_path, 'w')
    
    f_input = Path(input_path)
    if not f_input.is_file():
        raise FileNotFoundError(f"Input file {input_path} not found.")
        
    ts = np.loadtxt(f_input, dtype=float)
    vg = NaturalVisibilityGraph(ts)
    
    degrees = True
    if output_mode == 'el':
        es = vg.edgelist
        for a, b in es:
            print(a, b, file=f_output)
    elif output_mode == 'ds':
        ds = vg.degree_sequence
        for d in ds:
            print(d, file=f_output)
    elif output_mode == 'dd':
        ks, pks = vg.degree_distribution
        for k, pk in zip(ks, pks):
            print(k, pk, file=f_output)
    elif output_mode == 'dc':
        ks, nks = vg.degree_counts
        for k, nk in zip(ks, nks):
            print(k, nk, file=f_output)
    
    if output_path is not None:
        f_output.close()
        #print(f"Obtained visibility graph with {vg.vcount()} nodes and {vg.ecount()} edges")
        print(f"Saved {output_modes[output_mode]} to file: {output_path}")
