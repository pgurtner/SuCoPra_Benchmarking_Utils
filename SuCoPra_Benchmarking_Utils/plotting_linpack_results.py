import matplotlib.pyplot as plt
import numpy as np
from .extracting_linpack_results import extract_linpack_results

"""
@param plot_file_path: file path of output plot
@param hpl_file_paths: list of HPL.out file paths
@param wanted_fields: list of ...
@param x: {label: string, parse: records -> List}
@param y: {label: string, parse: records -> List}
@param lines: List{ value: number, orientation?: 'h|v', label: string, c?: 'color' }
"""
def plot_linpack (plot_file_path, hpl_file_paths, wanted_fields, x_axis, y_axis, lines=[]):
    records = extract_linpack_results(hpl_file_paths, wanted_fields)

    plt.xlabel(x_axis['label'])
    plt.ylabel(y_axis['label'])

    xpoints = np.array(list(map(x_axis['parse'], records)))
    ypoints = np.array(list(map(y_axis['parse'], records)))

    plt.plot(xpoints, ypoints, marker='.')

    plt.grid(visible=True)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    colors_counter = 0

    for line in lines:
        color = 'b'
        if 'color' in line:
            color = line['color']
        else:
            color = colors[colors_counter]
            colors_counter = (colors_counter + 1) % len(colors)

        if 'orientation' not in 'h' or line['orientation'] == 'h':
            plt.axhline(line['value'], label=line['label'], c=color)
        elif line['orientation'] == 'v':
            plt.axvline(line['value'], label=line['label'], c=color)

    if len(lines) > 0:
        plt.legend()

    plt.savefig(plot_file_path)

def parse_n (record):
    return _parse_int(record['N'])

def parse_nb (record):
    return _parse_int(record['NB'])

def parse_gflops (record):
    return _parse_float(record['Gflops'])

def parse_pq_to_nodes (record, mpi_per_node=2):
    return parse_pq_to_mpi(record)/mpi_per_node;

def parse_pq_to_mpi (record):
    p = _parse_int(record['P'])
    q = _parse_int(record['Q'])
    return p*q

def _parse_int (value):
    return int(value)

def _parse_float (value):
    return float(value)
