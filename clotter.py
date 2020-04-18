#!/usr/bin/python3 

import argparse
import datetime
import sys
import re
from collections import namedtuple
import matplotlib.pyplot as plt
import termplotlib as tpl

"""A wrapper script for matplotlib for plot graphs from the cmdline

Plan:
[x] Take a variable stream of data without header.
[x] Take a variable stream with header
    [x] parse option from commandline
    [x] use header parameters to lable graph
[x] Plot either directly to the commandline or to graphs
    [x] parse option from commandline to determine which
[] Deal with datetimes!
[] Autodump to /tmp

"""

testdata = [(1, 2),(2, 3),(3, 4)]

def parse_input(row, data=False):
    splitrow = row.split(',')
    x = [letter for letter in splitrow[-1].split()]
    splitrow[-1] = "".join(x)
    if data:
        splitrow = [int(v) for v in splitrow]
    else:
        splitrow = [v.strip() for v in splitrow]
    return splitrow

def process_stream(data):
    return [*zip(*data)]

def plot_data(data, headers, show=False):

    mfig = plt.figure()
    tfig = tpl.figure()

    x = data[0]
    for i, data in enumerate(data):
        if i == 0:
            x = data
            continue
        else:
            plt.plot(x, data, label=headers[i])
            tfig.plot(x, data, label=headers[i])
    plt.legend()
    plt.savefig('/tmp/{}-{}.jpeg'.format("".join(headers), datetime.datetime.now().isoformat(timespec='minutes')), format='jpeg')
    if show:
        plt.show()
    else:
        tfig.show()


def process(header=False):

    if header:
        headers = []
        for row in sys.stdin:
            headers = list(parse_input(row))
            break

    parsedinput = [ parse_input(row, data=True) for row in sys.stdin]
    dataforplotting = process_stream(parsedinput)
    plot_data(dataforplotting, headers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--header", help="specify if there is a header or not in the stream", action="store_true")
    parser.add_argument("--show", help="display the matplotlib figure immediately", action="store_true")
    args = parser.parse_args()
    sys.exit(process(args))

