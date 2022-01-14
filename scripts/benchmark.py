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

    sample_data = get_median_filtered(np.array(sample_delta))

    # Get the first element
    prev_val = sample_data[0]
    log['data'].append({
        'sec': sample_time[0],
        'val': prev_val
    })

    for i in range(1, len(sample_time) - 1):
        sec = sample_time[i]
        val = sample_data[i]
        if prev_val != val:
            prev_val = val
            log['data'].append({
                'sec': sec,
                'val': val
            })

    # Get the last element
    log['data'].append({
        'sec': sample_time[-1],
        'val': sample_data[-1]
    })

    return log

def process_csv(name, filename, do = "deltas"):
    
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        tracker = Tracker();
        for row in reader:
            tracker.addSample(row['track'], Sample( float(row['timeStampMs']), float(row['durationMs'])) )
        
    tracker.processDeltas()

    log_frame = {}
    log_frame['name'] = name + ":frame"
    log_frame['data'] = []
    log_frame['mean'] = tracker.delta_mean
    log_frame['median'] = tracker.delta_median
    sample_time = tracker.timestamps 
    sample_data = tracker.deltas

    for i in range(1, len(sample_time)):
        if  sample_data[i] > 0.0 and sample_data[i] != sample_data[i-1]:
            log_frame['data'].append({
                'sec': sample_time[i] * 0.001,
                'val': sample_data[i]
            })


    if do == "deltas":
        return log_frame

    elif do == "all":
        logs = [ ]
        # logs.append( log_frame )

        for track_name in tracker.getTracks():

            if track_name == "render":
                continue

            tracker.tracks[track_name].processDeltas()
            tracker.tracks[track_name].processDurations()

            log_track = {}
            log_track['name'] = name + "_" + track_name
            log_track['data'] = []
            log_track['mean'] = tracker.tracks[track_name].duration_mean
            log_track['median'] = tracker.tracks[track_name].duration_median

            print("processing", track_name, "mean:", log_track['mean'], "median:", log_track['median'] )
            
            sample_time = tracker.tracks[track_name].getTimestamps()
            sample_data = tracker.tracks[track_name].getDurations()
            # sample_data = tracker.tracks[track_name].durations_smooth
            for i in range(1, len(sample_time)):
                if  sample_data[i] > 0.0:
                    log_track['data'].append({
                        'sec': sample_time[i] * 0.001,
                        'val': sample_data[i]
                    })

            logs.append( log_track )

        return logs


def benchmark(name, shader_file, options, cwd = "./"):
    gv = GlslViewer(shader_file, options)

    gv.cmd.append("--fullFps")
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
    
    # subprocess.call(cmd, cwd=cwd, shell=True)
    return process_csv(name, cwd + "/" + name + ".csv", "all")

    # gv.start()
    # duration = 6
    # record_from = 2
    # data = []
    # data = gv.test(duration, record_from)
    # gv.stop()
    # return process_results(name, data)


