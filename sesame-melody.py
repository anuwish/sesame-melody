#!/usr/bin/env python

#import pyaudio
import aubio
import numpy as np
import pysoundcard as psc
from collections import deque
from itertools import groupby
import threading, time, difflib, random, struct, os

# configuration
try:
    import alsaaudio
    mixer = alsaaudio.Mixer(control='Mic', cardindex=0)
    mixer.setrec(1)
    mixer.setvolume(75, 0, alsaaudio.PCM_CAPTURE)
except:
    pass

# sound sources
class SourceFile:
    def __init__(self, filename, sample_rate, hop_size):
        self.filename = filename
        self.sample_rate = sample_rate
        self.hop_size = hop_size
        self.aubio_source = aubio.source(self.filename, self.sample_rate, self.hop_size)
    def get_next_chunk(self):
        samples, read = self.aubio_source()
        return samples

# TODO: find options to get it running on the raspberry pi
class AlsaSoundcard:
    def __init__(self, sample_rate, hop_size, input_device=True):
        self.sample_rate = int(sample_rate)
        self.hop_size = hop_size
        self.input_device = input_device
        self.framesize = int(940*float(self.sample_rate)/44100.0)
        self.stream = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, device='sysdefault:CARD=Headset')
        self.stream.setchannels(1)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_FLOAT_LE)
        self.stream.setperiodsize(self.framesize)

    def get_next_chunk(self):
        length = 0
        data = None
        while length <= 0:
            [length, data] = self.stream.read()
        floats = np.array(struct.unpack('f'*self.framesize,data),dtype=np.float32)
        return floats

    def start(self):
        pass

    def stop(self):
        pass

    def __del__(self):
        self.stop()


# TODO: find options to get it running on the raspberry pi
class SourceSoundcard:
    def __init__(self, sample_rate, hop_size, input_device=True):
        self.sample_rate = sample_rate
        self.hop_size = 1024
        self.input_device = input_device
        self.stream = psc.Stream(block_length=16,
                                 sample_rate=self.sample_rate,
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


# target melody, bar 6 to 13
def get_target_pitch():
    target_pitch = [
        "C6", "B5", "F5",                           # bar 06
        "A5", "G5", "F5", "D5",                     # bar 07
        "C5", "D5", "G4", "D5",                     # bar 08
        "E5", "C4", "E4", "G4", "C5", "E5", "G5",   # bar 09
        "C6", "B5", "F5",                           # bar 10
        "A5", "G5", "F5", "D5",                     # bar 11
        "C5", "E5", "D5", "E5",                     # bar 12
        "D5", "C5"                                  # bar 13
    ]
    return target_pitch

def get_target_pitch_midi():
    target_pitch = [
        84, 83, 77,                   # bar 06
        81, 79, 77, 74,               # bar 07
        72, 74, 67, 74,               # bar 08
        76, 60, 64, 67, 72, 76, 79,   # bar 09
        84, 83, 77,                   # bar 10
        81, 79, 77, 74,               # bar 11
        72, 76, 74, 76,               # bar 12
        74, 72                        # bar 13
    ]
    return target_pitch

def get_target_pitch_freq():
    target_pitch = [
        1046.5, 987.77, 698.46,                           # bar 06
        880.00, 783.99, 698.46, 587.33,                     # bar 07
        523.25, 587.33, 392.00, 587.33,                     # bar 08
        659.26, 261.63, 329.63, 392.00, 523.25, 659.26, 783.99,   # bar 09
        1046.5, 987.77, 698.46,                           # bar 10
        880.00, 783.99, 698.46, 587.33,                     # bar 11
        523.25, 659.26, 587.33, 659.26,                     # bar 12
        587.33, 523.25                                  # bar 13
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

#configure level detection
def create_level_alg(silence_threshold = -90. ):
    return LevelAlg(silence_threshold)

# Level Detection class wrapper
class LevelAlg:
    def __init__(self, silence_threshold):
        self.silence_threshold = silence_threshold
        self.level_detection_alg = aubio.level_detection
    def __call__(self, chunk):
        return self.level_detection_alg(chunk, self.silence_threshold)

class NoteDetector(threading.Thread):
    def __init__(self, source, dq,
                 hopsize=256,
                 sample_rate=44100,
                 onset_method="default",
                 onset_buffersize=512,
                 onset_threshold=0.1,
                 pitch_method="default",
                 pitch_unit="midi",
                 pitch_buffersize=4*512,
                 pitch_tolerance=0.8,
                 silence_threshold=-60.,
                 ):
        super(NoteDetector, self).__init__()
        self.source = source
        self.dq_external = dq
        self.onset_method = onset_method
        self.onset_buffersize = onset_buffersize
        self.onset_hopsize = hopsize
        self.onset_samplerate = sample_rate
        self.onset_threshold = onset_threshold
        self.pitch_method = pitch_method
        self.pitch_unit = pitch_unit
        self.pitch_buffersize = pitch_buffersize
        self.pitch_hopsize = hopsize
        self.pitch_samplerate = sample_rate
        self.pitch_tolerance = pitch_tolerance
        self.silence_threshold = silence_threshold
        self.pitch_alg = create_pitch_alg(self.pitch_method,
                                          self.pitch_buffersize,
                                          self.pitch_hopsize,
                                          self.pitch_samplerate,
                                          self.pitch_tolerance,
                                          self.pitch_unit)
        self.onset_alg = create_onset_alg(self.onset_method,
                                          self.onset_buffersize,
                                          self.onset_hopsize,
                                          self.onset_samplerate,
                                          self.onset_threshold)
        self.level_alg = create_level_alg(self.silence_threshold)

    def run(self):
        median_buffer = [ ]
        run = True
        found_onset = False
        while run:
            samples = self.source.get_next_chunk()
            level = self.level_alg(samples)
            onset = self.onset_alg(samples)[0]
            pitch = self.pitch_alg(samples)[0]
            confidence = self.pitch_alg.get_confidence()
            # check for onset
            if not found_onset:
                if onset > 0. and level is not 1.:
                    #print "Found an onset! Starting to fill the buffer!"
                    found_onset = True
                    median_buffer.append(pitch)
                    #print(onset, pitch, confidence, level)
                continue
            else:
                if onset > 0. or level is 1.:
                    #print "Found a new onset or silence! Start analysing notes in buffer."
                    if median_buffer: # check that buffer is not empty
                        med_pitch_array = np.around(np.array(median_buffer))
                        med_pitch = np.median(med_pitch_array)
                        self.dq_external.append(med_pitch)
                        # print med_pitch_array
                        # print med_pitch
                    median_buffer = []
                else:
                    if not pitch == 0.0 and not confidence < 0.6:
                        median_buffer.append(pitch)
                    #print(onset, pitch, confidence, level)
                continue
            # if confidence>0.9:
            #     #print(onset, pitch, confidence)
            #     self.dq_external.append((onset, pitch, confidence))

        #     pitches += [pitch]
        #     confidences += [confidence]
        #     # total_frames += read
        #     # if read < opts.hop_size: break
        #
        # skip = 1 # skip the first note
        # pitches = np.array(pitches[skip:])
        # confidences = np.array(confidences[skip:])
        # times = [t * opts.hop_size for t in range(len(pitches))]



def dummy(dq):
    l_detect = [
        (85.0, 1),
        (84.0, 111),
        (83.0, 123),
        (77.0, 37),
        (65.0, 1),
        (81.0, 2),
        (69.0, 16),
        (81.0, 33),
        (79.0, 79),
        (77.0, 81),
        (74.0, 78),
        (72.0, 164),
        (74.0, 80),
        (67.0, 59),
        (74.0, 16),
        (76.0, 78),
        (60.0, 33),
        (64.0, 22),
        (67.0, 36),
        (72.0, 29),
        (76.0, 37),
        (79.0, 4),
        (67.0, 11),
        (84.0, 109),
        (83.0, 118),
        (77.0, 38),
        (81.0, 9),
        (69.0, 6),
        (81.0, 4),
        (69.0, 4),
        (81.0, 34),
        (79.0, 79),
        (77.0, 80),
        (74.0, 2),
        (62.0, 1),
        (74.0, 76),
        (72.0, 167),
        (76.0, 81),
        (74.0, 59),
        (76.0, 17),
        (74.0, 149),
        (72.0, 1),
    ]
    print "DUMMY MODE"
    for i in range(0,random.randint(0, 100)):
        tone = random.randint(72, 90)
        dq.append(tone)
        time.sleep(0.1)
    print "Noise done."
    for p in l_detect:
        dq.append(p[0])
        time.sleep(0.1)
    print "Sequence done."
    for i in range(0,random.randint(0, 100)):
        tone = random.randint(72, 90)
        dq.append(tone)
        time.sleep(0.1)
    print "Noise done."
    while True:
        time.sleep(1)

class AnalyzeThread(threading.Thread):
    def __init__(self,dq):
        super(AnalyzeThread, self).__init__()
        self.dq_external=dq
        self.number_notes_consider = int(31*1.10)
        self.dq_ana = deque(maxlen=self.number_notes_consider)
        self.dq_ana_lo = deque(maxlen=self.number_notes_consider)
        self.dq_ana_hi = deque(maxlen=self.number_notes_consider)
        self.threshold_detected = 0.65
        self.max_ratio = 0.0
        self.sleep_timer = 0.1
        self.target_pitch = get_target_pitch_midi()
        self.base_notes_only = False

    def run(self):
        if self.base_notes_only:
            self.target_pitch[:] = [x % 12 for x in self.target_pitch]
            print self.target_pitch
        perform_analysis = False
        while True:
            if len(self.dq_external) > 0:
                # Feed new notes to own analysis deque
                while len(self.dq_external) > 0:
                    tone = self.dq_external.popleft()
                    if self.base_notes_only:
                        tone = tone%12
                    self.dq_ana.append(tone)
                    self.dq_ana_lo.append(tone-1.0)
                    self.dq_ana_hi.append(tone+1.0)
                perform_analysis = True
            else:
                time.sleep(self.sleep_timer)

            if perform_analysis:
                perform_analysis = False
                list_tones = list(self.dq_ana)
                list_tones_lo = list(self.dq_ana_lo)
                list_tones_hi = list(self.dq_ana_hi)
                sm=difflib.SequenceMatcher(None,self.target_pitch,list_tones)
                sm_lo=difflib.SequenceMatcher(None,self.target_pitch,list_tones_lo)
                sm_hi=difflib.SequenceMatcher(None,self.target_pitch,list_tones_hi)
                if sm.ratio() > self.max_ratio:
                    self.max_ratio = sm.ratio()
                print "CL: " + str(sm.ratio()) + " @" + str(list_tones)
                print "CL (lo): " + str(sm_lo.ratio()) + " @" + str(list_tones_lo)
                print "CL (hi): " + str(sm_hi.ratio()) + " @" + str(list_tones_hi)
                print
                #print sm.ratio()
                if max(sm.ratio(), sm_lo.ratio(), sm_hi.ratio()) > self.threshold_detected:
                    print ""
                    print ""
                    print ""
                    print "YEAH! DETECTED @" + str(sm.ratio()) + " (max: " + str(self.max_ratio) + ")"
                    print "Analyzed list: "
                    print list_tones
                    print ""
                    print ""
                    print ""
                    self.dq_ana.clear()
                    self.dq_ana_lo.clear()
                    self.dq_ana_hi.clear()

def main(opts):
    # inspired by aubionotes.c

    input_device_pi = {
       'default_high_input_latency': 0.046439909297052155,
       'default_high_output_latency': 0.046439909297052155,
       'default_low_input_latency': 0.042653061224489794,
       'default_low_output_latency': 0.042653061224489794,
       'default_sample_rate': opts.sample_rate,
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



    input_device = True
    if opts.pi:
        input_device = input_device_pi

    source = None
    if opts.filename is not None:
        source = SourceFile(opts.filename, opts.sample_rate, opts.hop_size)
    else:
        if opts.soundinterface == "alsa" and not opts.dummy:
            source = AlsaSoundcard(opts.sample_rate, opts.hop_size, input_device)
        elif opts.soundinterface == "pysoundcard" and not opts.dummy:
            source = SourceSoundcard(opts.sample_rate, opts.hop_size, input_device)

    dq_alltones = deque(maxlen=10000)

    analyser = AnalyzeThread(dq_alltones)
    analyser.daemon = True
    analyser.start()

    if opts.dummy:
        dummy(dq_alltones)
    else:
        notedetect = NoteDetector(source, dq_alltones,
                                  hopsize=opts.hop_size,
                                  sample_rate=opts.sample_rate,
                                  onset_method=opts.onset_method,
                                  onset_buffersize=opts.buffer_size,
                                  onset_threshold=opts.onset_threshold,
                                  pitch_method=opts.pitch_method,
                                  pitch_unit=opts.pitch_unit,
                                  pitch_buffersize=(opts.buffer_size*opts.pitch_to_onsetbuffer_ratio),
                                  pitch_tolerance=opts.pitch_tolerance,
                                  silence_threshold=opts.silence_threshold
                                  )
        notedetect.daemon = True
        notedetect.start()


    try:
        while True: time.sleep(0.2)
    except (KeyboardInterrupt, SystemExit):
        print '\n! Received keyboard interrupt, quitting threads.\n'

    return


def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

import sys
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sesame Melody - Note detection")
    parser.add_argument("-f", "--file", dest="filename", default=None,
                        help="input file (.wav)", metavar="FILE")
    parser.add_argument("-p", "--pi", dest='pi', action='store_true')
    parser.add_argument("-s", "--soundinterface", dest='soundinterface', metavar="INTERFACE",
                        type=str, choices=["alsa","pysoundcard"], default="alsa",
                        help="choose soundcard interface")
    parser.add_argument("--sample-rate", dest="sample_rate", metavar="RATE",
                        type=int, default=44100,
                        help="sample rate in Hz")
    parser.add_argument("--hop-size", dest="hop_size", metavar="HOP",
                        type=int, default=256,
                        help="hop size in bits")
    parser.add_argument("--buffer-size", dest="buffer_size", metavar="BUFFER_SIZE", default=512)
    parser.add_argument("--pitch-to-onsetbuffer-ratio",
                        dest="pitch_to_onsetbuffer_ratio", metavar="RATIO",
                        type=int, default=4)
    parser.add_argument("--pitch-method", dest="pitch_method", metavar="PITCH_METHOD",
                        type=str,
                        choices=["default","schmitt","fcomb","mcomb","specacf","yin","yinfft"],
                        default="default")
    parser.add_argument("--pitch-unit", dest="pitch_unit", metavar="PITCH_UNIT",
                        type=str, choices=["midi","bin","cent","Hz"], default="midi")
    parser.add_argument("--pitch-tolerance", dest="pitch_tolerance", metavar="PITCH_TOLERANCE",
                        type=restricted_float, default=0.8)
    parser.add_argument("--onset-method", dest="onset_method", metavar="ONSET_METHOD",
                        type=str,
                        choices=["default","energy","hfc","complex","phase","specdiff","kl","mkl","specflux"],
                        default="default")
    parser.add_argument("--onset-threshold", dest="onset_threshold", metavar="ONSET_THRESHOLD",
                        type=restricted_float, default=0.1)
    parser.add_argument("--silence-threshold", dest="silence_threshold", metavar="SILENCE_THRESHOLD",
                        type=float, default=-50.,
                        help="""Set the silence threshold, in dB, under which
                             the pitch will not be detected. A value of -20.0
                             would eliminate most onsets but the loudest ones. A
                             value of -90.0 would select all onsets.""")
    parser.add_argument("-d", "--dummy", dest='dummy', action='store_true')




    opts = parser.parse_args()

    main(opts)
