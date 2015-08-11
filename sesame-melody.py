#!/usr/bin/env python

#import pyaudio
import aubio
import numpy as np
import pysoundcard as psc

# configuration
try:
    import alsaaudio
    mixer = alsaaudio.Mixer(control='Mic', cardindex=0)
    mixer.setrec(1)
    mixer.setvolume(80, 0, alsaaudio.PCM_CAPTURE)
except:
    pass

# target melody, bar 6 to 13
def get_target_pitch():
    target_pitch = [
        "C6", "B5", "F5",                           # bar 06
        "A5", "G5", "F5", "D5",                     # bar 07
        "C5", "D5", "G4", "D5",                     # bar 08
        "E4", "C4", "E4", "G4", "C5", "E5", "G5",   # bar 09
        "C6", "B5", "F5",                           # bar 10
        "A5", "G5", "F5", "D5",                     # bar 11
        "C5", "E5", "D5", "E5",                     # bar 12
        "D5", "C5"                                  # bar 13
    ]
    return target_pitch

def get_target_pitch_midi():
    target_pitch = [
        "84", "83", "77",                           # bar 06
        "81", "79", "77", "74",                     # bar 07
        "72", "74", "67", "74",                     # bar 08
        "64", "60", "64", "67", "72", "76", "79",   # bar 09
        "84", "83", "77",                           # bar 10
        "81", "79", "77", "74",                     # bar 11
        "72", "76", "74", "76",                     # bar 12
        "74", "72"                                  # bar 13
    ]
    return target_pitch



# configure pitch detection
def create_pitch_alg(pitch_method="default", pitch_buffer_size=4*512,
                     pitch_hop_size=256, pitch_samplerate=44100,
                     pitch_tolerance=0.8, pitch_unit="midi"):
    pitch_alg = aubio.pitch(pitch_method, pitch_buffer_size, pitch_hop_size, pitch_samplerate)
    pitch_alg.set_tolerance(pitch_tolerance)
    pitch_alg.set_unit(pitch_unit)
    return pitch_alg

# configure onset detection
def create_onset_alg(onset_method="default", onset_buffer_size=512,
                     onset_hop_size=256, onset_samplerate=44100,
                     onset_threshold=0.):
    onset_alg = aubio.onset(onset_method, onset_buffer_size, onset_hop_size, onset_samplerate)
    onset_alg.set_threshold(onset_threshold)
    return onset_alg



class SourceFile:
    def __init__(self, filename, samplerate, hop_size):
        self.filename = filename
        self.samplerate = samplerate
        self.hop_size = hop_size
        self.aubio_source = aubio.source(self.filename, self.samplerate, self.hop_size)
    def get_next_chunk(self):
        samples, read = self.aubio_source()
        return samples

# TODO: find options to get it running on the raspberry pi
class SourceSoundcard:
    def __init__(self, samplerate, hop_size, input_device=True):
        self.samplerate = samplerate
        self.hop_size = hop_size
        self.input_device = input_device
        self.stream = psc.Stream(block_length=self.hop_size,
                                 samplerate=self.samplerate,
                                 input_device=self.input_device)
        self.stream.start()
    def get_next_chunk(self):
        vec = self.stream.read(self.hop_size)
        # mix down to mono
        mono_vec = vec.sum(-1)/float(self.stream.input_channels)
        return mono_vec
    def start(self):
        if self.stream.is_stopped():
            self.stream.start()
    def stop(self):
        if self.stream.is_active():
            self.stream.stop()
    def __del__(self):
        self.stop()

def main(opts):
    # inspired by aubionotes.c

    input_device_pi = {
       'default_high_input_latency': 0.046439909297052155,
       'default_high_output_latency': 0.046439909297052155,
       'default_low_input_latency': 0.042653061224489794,
       'default_low_output_latency': 0.042653061224489794,
       'default_sample_rate': opts.samplerate,
       'device_index': 0,
       'host_api_index': 0,
       'input_channels': 1,
       'input_latency': 0.042653061224489794,
       'interleaved_data': True,
       'name': u'Logitech USB Headset: USB Audio (hw:0,0)',
       'output_channels': 2,
       'output_latency': 0.042653061224489794,
       'sample_format': np.float32,
       'struct_version': 2
    }


    pitch_alg = create_pitch_alg()
    onset_alg = create_onset_alg()

    #onset_vec = aubio.fvec(1)
    #pitch_vec = aubio.fvec(1)

    input_device = True
    if opts.pi:
        input_device = input_device_pi

    print input_device

    source = None
    if opts.filename is not None:
        source = SourceFile(opts.filename, opts.samplerate, opts.hop_size)
    else:
        source = SourceSoundcard(opts.samplerate, opts.hop_size, input_device)

    # TODO: Try to understand and rebuild aubionotes median implementation
    # # use median
    # use_median = True
    # median_size = 6



    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples = source.get_next_chunk()
        # samples, read = source.get_next_chunk()
        pitch = pitch_alg(samples)[0]
        confidence = pitch_alg.get_confidence()

        print(pitch, confidence)
        pitches += [pitch]
        confidences += [confidence]
        # total_frames += read
        # if read < opts.hop_size: break

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
    parser.add_argument("-p", "--pi", dest='pi', action='store_true')
    parser.add_argument("-R", "--samplerate", dest="samplerate", default=44100,
                        help="sample rate in Hz", metavar="RATE")
    parser.add_argument("-H", "--hopsize", dest="hop_size", default=256,
                        help="hop size in bits", metavar="HOP")

    opts = parser.parse_args()
    main(opts)
