#!/usr/bin/python

import datetime
import time
import re
import sys

import yaml
import numpy as np
import matplotlib
matplotlib.use('Agg') # png output
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

import tracker

def plot_dates(label, dates, values, output):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(dates, values, label=store_type, marker='o')
    # ax.plot_date(dates, values, ydate=False, label=store_type, marker='o')

    ax.grid(True)
    # plt.legend()
    fig.autofmt_xdate()
    plt.savefig(output)

if __name__ == "__main__":
    filter_to = False
    if len(sys.argv) > 1:
        filter_to = sys.argv[1]
    store = tracker.SequenceStore('data.sqlite')
    targets = yaml.load(open('targets.yaml'))
    for store_type in targets.iterkeys():
        # turn [(a, 1), (b, 2), (c, 3)] into (a,b,c),(1,2,3)
        if filter_to and not re.match(filter_to, store_type):
            continue
        dates, values = zip(*store.get(store_type, True, int))
        plot_dates(store_type, dates, values, store_type)