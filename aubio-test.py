import alsaaudio, struct
import aubio
from collections import deque
from copy import deepcopy
from itertools import groupby
 
# constants
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 11025
FRAMESIZE   = 235
FRAMESIZE_AUBIO = 235
PITCHALG    = "yin"
PITCHOUT    = "freq"

# audio levels 
AUDIO_GAIN  = 80
AUDIO_MIN_ENERGY = 0.1

# activate microphone and set gain
mixer = alsaaudio.Mixer(control='Mic', cardindex=0)
mixer.setrec(1)
mixer.setvolume(AUDIO_GAIN, 0, alsaaudio.PCM_CAPTURE)
 
# set up audio input
recorder=alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, device='sysdefault:CARD=Headset')
recorder.setchannels(CHANNELS)
recorder.setrate(RATE)
recorder.setformat(INFORMAT)
recorder.setperiodsize(FRAMESIZE)

# set up pitch detect
# detect = new_aubio_pitchdetection(FRAMESIZE_AUBIO,FRAMESIZE_AUBIO/2,CHANNELS,
#                                   RATE,PITCHALG,PITCHOUT)
detect = aubio.pitch(PITCHALG, FRAMESIZE_AUBIO,FRAMESIZE_AUBIO/2,RATE)#
detect.set_tolerance(0.8)
detect.set_unit(PITCHOUT)

#buf = new_fvec(FRAMESIZE_AUBIO,CHANNELS)

tone_dist = 2.0**(1.0/12.0)
tonedict = {
  440.0*tone_dist**-36 : ",A",
  440.0*tone_dist**-35 : ",B",
  440.0*tone_dist**-34 : ",H",
  440.0*tone_dist**-33 : "C",
  440.0*tone_dist**-32 : "Cis",
  440.0*tone_dist**-31 : "D",
  440.0*tone_dist**-30 : "Dis",
  440.0*tone_dist**-29 : "E",
  440.0*tone_dist**-28 : "F",
  440.0*tone_dist**-27 : "Fis",
  440.0*tone_dist**-26 : "G",
  440.0*tone_dist**-25 : "Gis",
  440.0*tone_dist**-24 : "A",
  440.0*tone_dist**-23 : "B",
  440.0*tone_dist**-22 : "H",
  440.0*tone_dist**-21 : "c",
  440.0*tone_dist**-20 : "cis",
  440.0*tone_dist**-19 : "d",
  440.0*tone_dist**-18 : "dis",
  440.0*tone_dist**-17 : "e",
  440.0*tone_dist**-16 : "f",
  440.0*tone_dist**-15 : "fis",
  440.0*tone_dist**-14 : "g",
  440.0*tone_dist**-13 : "gis",
  440.0*tone_dist**-12 : "a",
  440.0*tone_dist**-11 : "b",
  440.0*tone_dist**-10 : "h",
  440.0*tone_dist**-9  : "c'",
  440.0*tone_dist**-8  : "cis'",
  440.0*tone_dist**-7  : "d'",
  440.0*tone_dist**-6  : "dis'",
  440.0*tone_dist**-5  : "e'",
  440.0*tone_dist**-4  : "f'",
  440.0*tone_dist**-3  : "fis'",
  440.0*tone_dist**-2  : "g'",
  440.0*tone_dist**-1  : "gis'",
  440.0*tone_dist**0   : "a'",
  440.0*tone_dist**1   : "b'",
  440.0*tone_dist**2   : "h'",
  440.0*tone_dist**3   : "c2",
  440.0*tone_dist**4   : "cis2",
  440.0*tone_dist**5   : "d2",
  440.0*tone_dist**6   : "dis2",
  440.0*tone_dist**7   : "e2",
  440.0*tone_dist**8   : "f2",
  440.0*tone_dist**9   : "fis2",
  440.0*tone_dist**10  : "g2",
  440.0*tone_dist**11  : "gis2",
  440.0*tone_dist**12  : "a2",
  440.0*tone_dist**13  : "b2",
  440.0*tone_dist**14  : "h''",
  440.0*tone_dist**15  : "c3",
  440.0*tone_dist**16  : "cis3",
  440.0*tone_dist**17  : "d3",
  440.0*tone_dist**18  : "dis3",
  440.0*tone_dist**19  : "e3",
  440.0*tone_dist**20  : "f3",
  440.0*tone_dist**21  : "fis3",
  440.0*tone_dist**22  : "g3",
  440.0*tone_dist**23  : "gis3",
  440.0*tone_dist**24  : "a3",
  440.0*tone_dist**25  : "b3",
  440.0*tone_dist**26  : "h3",
  440.0*tone_dist**27  : "c4",
  440.0*tone_dist**28  : "cis4",
  440.0*tone_dist**29  : "d4",
  440.0*tone_dist**30  : "dis4",
  440.0*tone_dist**31  : "e4",
  440.0*tone_dist**32  : "f4",
  440.0*tone_dist**33  : "fis4",
  440.0*tone_dist**34  : "g4",
  440.0*tone_dist**35  : "gis4",
  440.0*tone_dist**36  : "a4",
}

def tone_unified(s):
  return s.strip("'").strip(",").strip("1").strip("2").strip("3").strip("4").upper()

def freq2tonestr(freq,energy):
  for f,s in tonedict.iteritems():
    rel_dist = (f-freq)/f
    if abs(rel_dist) < 0.03:
      return "{:>10} ({:10.4f}),   f={:10.4f},   e={:10.4f},   r={:10.4f}".format(tone_unified(s),f,freq,energy,rel_dist)
  return     "{:>10} ({:10.4f}),   f={:10.4f},   e={:10.4f}".format("---", 0, freq, energy)


def freq2tone(freq,energy):
  for f,s in tonedict.iteritems():
    rel_dist = (f-freq)/f
    if abs(rel_dist) < 0.03:
      return (tone_unified(s),f,freq,energy,rel_dist)
  return ("---",0,freq,energy,0)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# main loop
runflag = 1
dq_alltones = deque(maxlen=100)
last_tone = (None, None)
update = True
while runflag:
 
  # read data from audio input
  [length, data]=recorder.read()
  #print length

  if length > 0:
    #print length
 
    # convert to an array of floats
    floats = struct.unpack('f'*FRAMESIZE,data)

    #cc = chunks(floats, 235) 

    #for c in cc:
    # copy floats into structure
    # for i in range(len(floats)):
    #   fvec_write_sample(buf, floats[i], 0, i)

    # find pitch of audio frame
    freq = aubio_pitchdetection(detect,buf)
    #ovec = None
    #aubio_onsetdetection(onset, ovec)

    # find energy of audio frame
    energy = vec_local_energy(buf)

    if freq != RATE and energy>AUDIO_MIN_ENERGY:
      print "   last tone: " + freq2tonestr(freq, energy)
      #print freq2tone(freq, energy)
      tone = freq2tone(freq, energy)
      if (tone[0] == last_tone[0]):
        dq_alltones.append(last_tone)
        update = True
      last_tone = deepcopy(tone)
      #print dq
  
  if update:
    list_tones = [(a,b) for (a,b) in [(key,len(list(group))) for key, group in groupby(dq_alltones, lambda x: x[0])] if b>0]
    print " tone sequence: " + str(list_tones)
    update = False



