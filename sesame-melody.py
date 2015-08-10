#!/usr/bin/env python

import pyaudio as pa
import aubio as ab
import numpy as np

# configuration

# target melody, bar 6 to 13
def get_target_pitch():
    target_pitch = [
        "c3", "h2", "f2",                           # bar 06
        "a2", "g2", "f2", "d2",                     # bar 07
        "c2", "d2", "g1", "d2",                     # bar 08
        "e1", "c1", "e1", "g1", "c2", "e2", "g2",   # bar 09
        "c3", "h2", "f2",                           # bar 10
        "a2", "g2", "f2", "d2",                     # bar 11
        "c2", "e2", "d2", "e2",                     # bar 12
        "d2", "c2"                                  # bar 13
    ]
    return target_pitch


# configure pitch detection
def create_pitch_alg(pitch_method="default", pitch_buffer_size=4*512,
                     pitch_hop_size=256, pitch_samplerate=44100,
                     pitch_tolerance=0.8, pitch_unit="midi"):
    pitch_alg = ab.pitch(pitch_method, pitch_buffer_size, pitch_hop_size, pitch_samplerate)
    pitch_alg.set_tolerance(pitch_tolerance)
    pitch_alg.set_unit(pitch_unit)
    return pitch_alg

# configure onset detection
def create_onset_alg(onset_method="default", onset_buffer_size=512,
                     onset_hop_size=256, onset_samplerate=44100,
                     onset_threshold=0.):
    onset_alg = ab.onset(onset_method, onset_buffer_size, onset_hop_size, onset_samplerate)
    onset_alg.set_threshold(onset_threshold)
    return onset_alg

def main(opts):
    print "Do nothing serious"
    # inspired by aubionotes.c

    pitch_alg = create_pitch_alg()
    onset_alg = create_onset_alg()

    onset_vec = ab.fvec(1)
    pitch_vec = ab.fvec(1)

    source = None
    if opts.filename is not None:
        source = ab.source(opts.filename, opts.samplerate, opts.hop_size)

    # use median
    use_median = True
    median_size = 6



    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = source()
        pitch = pitch_alg(samples)[0]
        confidence = pitch_alg.get_confidence()
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < opts.hop_size: break

    print pitches
    skip = 1 # skip the first note
    pitches = np.array(pitches[skip:])
    confidences = np.array(confidences[skip:])
    times = [t * opts.hop_size for t in range(len(pitches))]

    print pitches
    return



import sys
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sesame Melody - Note detection")
    parser.add_argument("-f", "--file", dest="filename", default=None,
                        help="input file (.wav)", metavar="FILE")
    parser.add_argument("-R", "--samplerate", dest="samplerate", default=44100,
                        help="sample rate in Hz", metavar="RATE")
    parser.add_argument("-H", "--hopsize", dest="hop_size", default=256,
                        help="hop size in bits", metavar="HOP")

    opts = parser.parse_args()
    main(opts)
