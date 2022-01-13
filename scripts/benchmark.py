#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import csv
import numpy as np
import subprocess

from stats import get_median_filtered
from tracker import Tracker, Sample
from glslviewer import GlslViewer

def process_results(name, results):
    log = {}

    # Prepare averages
    sample_delta = []
    sample_time = []
    # prev_val = 0.0
    for sample in results:
        sample_time.append(sample['time'])
        sample_delta.append(sample['delta'])

    log['name'] = name
    log['data'] = []
    log['mean'] = np.mean(sample_delta)
    log['median'] = np.median(sample_delta)

    sample_smoothdelta = get_median_filtered(np.array(sample_delta))

    # Get the first element
    prev_val = sample_smoothdelta[0]
    log['data'].append({
        'sec': sample_time[0],
        'val': prev_val
    })

    for i in range(1, len(sample_time) - 1):
        sec = sample_time[i]
        val = sample_smoothdelta[i]
        if prev_val != val:
            prev_val = val
            log['data'].append({
                'sec': sec,
                'val': val
            })

    # Get the last element
    log['data'].append({
        'sec': sample_time[-1],
        'val': sample_smoothdelta[-1]
    })

    return log

def process_csv(name, filename):
    log = {}

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        tracker = Tracker();
        for row in reader:
            tracker.addSample(row['track'], Sample( float(row['timeStampMs']), float(row['durationMs'])) )
        
    tracker.processDeltas()

    log['name'] = name
    log['data'] = []
    log['mean'] = tracker.delta_mean
    log['median'] = tracker.delta_median
    sample_time = tracker.timestamps
    sample_smoothdelta = tracker.deltas_smooth

    # Get the first element
    prev_val = sample_smoothdelta[0]
    log['data'].append({
        'sec': sample_time[0],
        'val': prev_val
    })

    for i in range(1, len(sample_time) - 1):
        sec = sample_time[i]
        val = sample_smoothdelta[i]
        if prev_val != val:
            prev_val = val
            log['data'].append({
                'sec': sec,
                'val': val
            })

    # Get the last element
    log['data'].append({
        'sec': sample_time[-1],
        'val': sample_smoothdelta[-1]
    })

    return log


def benchmark(name, shader_file, options, cwd = "./"):
    gv = GlslViewer(shader_file, options)

    gv.cmd.append("-e")
    gv.cmd.append("track,on")
    gv.cmd.append("-e")
    gv.cmd.append("wait,10")
    gv.cmd.append("-e")
    gv.cmd.append("track,off")
    gv.cmd.append("-e")
    gv.cmd.append("track,samples," + name + ".csv")
    gv.cmd.append("-e")
    gv.cmd.append("track,average")
    gv.cmd.append("-E")
    gv.cmd.append("screenshot," + name + ".png")

    cmd = gv.getCommand()
    # print(cmd)
    
    subprocess.call(cmd, cwd=cwd, shell=True)
    return process_csv(name, cwd + "/" + name + ".csv")

    # gv.start()
    # duration = 6
    # record_from = 2
    # data = []
    # data = gv.test(duration, record_from)
    # gv.stop()
    # return process_results(name, data)


