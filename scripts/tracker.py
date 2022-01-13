#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

from stats import get_median_filtered

class Sample:
    timestamp: float    = 0
    duration: float     = 0
    delta: float        = 0

    def __init__(self, timestamp, duration):
        self.timestamp = timestamp
        self.duration = duration


class Track:
    name: str
    samples = []

    deltas_smooth = []
    delta_median = 0
    delta_mean = 0
    deltas_processed = False

    durations_smooth = []
    duration_median = 0
    duration_mean = 0

    def __init__(self, name):
        self.name = name

    def processDeltas(self):
        i = 0
        deltas = []
        for sample in self.samples:
            if i > 0:
                sample.delta = sample.timestamp - self.samples[i-1].timestamp
            i += 1
            deltas.append(sample.delta)

        self.deltas_processed = True

        self.deltas_smooth = get_median_filtered( np.array(deltas) )
        self.delta_median = np.median(deltas)
        self.delta_mean = np.mean(deltas)

    def processDurations(self):
        durations = self.getDurations()
        self.durations_smooth = get_median_filtered( np.array(durations) )
        self.duration_median = np.median(durations)
        self.duration_mean = np.mean(durations)

    def getTimestamps(self):
        return [sample.timestamp for sample in self.samples]

    def getDurations(self):
        return [sample.duration for sample in self.samples]

    def getDeltas(self):
        if not self.deltas_processed:
            self.processDeltas()

        return [sample.delta for sample in self.samples]


class Tracker:
    tracks = {}

    timestamps = []
    deltas = []
    deltas_smooth = []
    delta_median = 0
    delta_mean = 0

    def addSample(self, track_name, sample: Sample): 
        if not track_name in self.tracks:
            self.tracks[track_name] = Track(track_name)

        self.tracks[track_name].samples.append( sample )

    def processDeltas(self):
        # samples = []
        # for track in self.tracks:
        #     self.tracks[track].processDeltas()
        #     for sample in self.tracks[track].samples:
        #         samples.append( [sample.timestamp, sample.delta] )

        # samples = sorted(samples, key=lambda x: x[0] )
        
        # self.timestamps = [delta_sample[0] for delta_sample in samples]
        # self.deltas = [delta_sample[1] for delta_sample in samples]

        self.tracks["render"].processDeltas()
        self.timestamps = [ sample.timestamp for sample in self.tracks["render"].samples ]
        self.deltas = [ sample.delta for sample in self.tracks["render"].samples ]

        self.delta_mean = np.mean(self.deltas)
        self.delta_median = np.median(self.deltas)
        self.deltas_smooth = get_median_filtered( np.array(self.deltas) )
