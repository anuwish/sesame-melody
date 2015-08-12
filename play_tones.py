#!/usr/bin/env python
"""Play a fixed frequency sound."""
from __future__ import division
import math

from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

def sine_tone(stream, frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

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

p = PyAudio()
stream = p.open(format=p.get_format_from_width(1), # 8bit
                channels=1, # mono
                rate=44100,
                output=True)
for f in get_target_pitch_freq():
    sine_tone(stream, frequency=f, duration=1, volume=0.1,sample_rate=44100)

stream.stop_stream()
stream.close()
p.terminate()
