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
def create_pitch_alg(pitch_method = "default", pitch_buffer_size = 4*512,
                     pitch_hop_size = 256, pitch_samplerate = 44100,
                     pitch_tolerance = 0., pitch_unit = "midi"):
    pitch_alg = ab.pitch(pitch_method, pitch_buffer_size, pitch_hop_size, pitch_samplerate)
    pitch_alg.set_tolerance(pitch_tolerance)
    pitch_alg.set_unit(pitch_unit)
    return pitch_alg

# configure onset detection
def create_onset_alg(onset_method = "default", onset_buffer_size = 512,
                     onset_hop_size = 256, onset_samplerate = 44100,
                     onset_threshold = 0.):
    onset_alg = ab.onset(onset_method, onset_buffer_size, onset_hop_size, onset_samplerate)
    onset_alg.set_threshold(onset_threshold)
    return onset_alg

def main(args):
    print "Do nothing serious"
    # inspired by aubionotes.c



    pitch_alg = create_pitch_alg()
    onset_alg = create_onset_alg()

    onset_vec = ab.fvec(1)
    pitch_vec = ab.fvec(1)

    # use median
    use_median = True
    median_size = 6



    return



import sys
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sesame Melody - Note detection")
    parser.add_argument("-f", "--file", dest ="filename",
                        help="input file (.wav)", metavar="FILE")

    opts = parser.parse_args()
    main(opts)
