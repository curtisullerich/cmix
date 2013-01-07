from rtcmix import *
from metalib import *
import math
#print_off()
rtsetparams(44100, 2)
load("STRUM2")

"""
from Chapter 16 (Mapping) of Notes from the Metalevel
"""

#plays notes on the STRUM2 instrument along a sine wave
def playsine(length, cycs, key1, key2, pulse, dur, amp):
  maxx = length - 1
  maxr = 2 * 3.14159 * cycs
  o = pulse
  for x in range(0, maxx):
    r = rescale(x, 0, maxx, 0, maxr)
    key = rescale(math.sin(r), -1, 1, key1, key2)
    k = keynumToHertz(key)
    print "hertz: " + str(k)
    STRUM2(pulse, dur, amp, k, 1, 1.0, 0.5)
    pulse = pulse + o

#chops a value in segments over several levels of recursion
def sschop (value, segments, levels):
  chopped = [value]
  if (value is 0):
    return []
  elif (levels < 1):
    return chopped
  else:
    nextval = value / segments
    nexlev = levels - 1
    for x in range(segments):
      chopped.extend(sschop( nextval, segments, nexlev ))
    return chopped

#melody is assumed to be a list of keynums
def sierpinski(tone, melody, levels, dur, amp, pulse, timepoint):
  length = len(melody)
  for i in melody:
    k=tone+i#tone is the base pitch. Transpose I above tone
    print "i=%i length=%i k=%i" % (i, length, k)    
    STRUM2(timepoint, dur, amp, keynumToHertz(k), 1, 1.0, 0.5)
    if (levels > 1):
      sierpinski(k+12, melody, levels-1, float(dur)/float(length), amp*.8, float(pulse)/float(length), timepoint)
    timepoint = timepoint + pulse

#length, cycles, lower key, higher key, pulse value, note duration, amplitude
#playsine(100, 4, 80, 100, .1, .3, 10000)
#playsine(100, 4, 50, 80, .1, .3,  9500)

#print str(sschop(8, 2, 4))
pulse = 1
sierpinski(40, [0, 4, 8], 4, 3, 10000, 3, 0)

