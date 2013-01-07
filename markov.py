from rtcmix import *
from metalib import *
import math
import random
#print_off()
rtsetparams(44100, 2)
load("STRUM2")

"""
from Chapter 19 (Markov Processes) of Notes from the Metalevel
"""

#both are valid dictionary instantiations
rhydict  = dict(
q=dict(q=.5,e=2,ed=.75),
e=dict(e=3,q=1),
ed=dict(s=1),s=dict(e=2,q=1)
)
rhydict2 = dict(
q=dict(q=.5,e=2,ed=.75,w=.2),
e=dict(e=3,q=1),ed=dict(s=1),
s=dict(e=2,q=1),
w=dict(stop=1)
)
rhydict3 = dict(
q=dict(q=.5,e=2,ed=1.5,w=.2),
e=dict(e=2.5,q=1),
ed=dict(s=1,ed=.3),
s=dict(e=2,q=1,s=3),
w=dict(stop=1)
)
intmix   = {
1:{3:.4,4:.4,6:.1},
2:{2:.2,3:.4,4:.4,6:.1},
3:{1:.2,2:.6,4:.4},
4:{2:.2,3:.4,4:.4},
6:{2:.4,3:.2,4:.2}
}
intmix2  = {
c4: {4:.2,7:.5,12:.3},
c7: {4:.1,7:.1,12:.1},
c12:{4:.2,7:.3,12:.4}
}

#Uses markov chains to generate rhythms for a drunk sequence of notes
#Use rhytable  for the first exercise from Metalevel
#and rhytable2 for the second exercise. This function works for both.
def markovRhythms(length, quarterNote, tbl):
  r =  'q'
  drunk = Drunk(60, 6, 40, 80, 3, 10)
  timepoint = 0
  amp = 10000
  pulse = quarterNote
  count = 0
  for i in range(length):
    k = drunk.next()
    r = selectNextFromDict(tbl, r)
    print "r=" + str(r)
    dur = pulse
    if r == 'q':
      dur = pulse
    elif r == 'e':
      dur = pulse/2.
    elif r == 'ed':
      dur = pulse / 2.
      dur = dur * 1.5
    elif r == 's':
      dur = pulse / 4.
    elif r == 'w':
      return
    STRUM2(timepoint, pulse, amp, keynumToHertz(k), 1, 1.0, 0.5)
    timepoint += dur

def markovChorder(length, intmix, note, size, ud, rhy, dur, begin):
  intt = begin
  key = note
  chord = False
  timepoint = 0
  for i in range(length):
    intt = selectNextFromDict(intmix, intt)
    if (random.random() < ud):
      key += intt
      if (key > 90):
        key = 90
    else:
      key -= intt
      if (key < 50):
        key = 50
    chord = []
    for i in range(size):
      n = key
      intt = selectNextFromDict(intmix, intt)
      n = n - intt
      chord.append(n)    
    for c in chord:
      STRUM2(timepoint, dur, 10000, keynumToHertz(c), 1, 1.0, 0.5)    
    timepoint += rhy

#select the next element of the markov transition table
#dictionary implementation given the past value
def selectNextFromDict(table, past):
  
  lesum = 0
  #print "past: " + str(past)
  #print "dict: " + str(table.get(past))
  for val in table.get(past).values():
    lesum += val
  #print "lesum: " + str(lesum)
  r = random.uniform(0, lesum)

  rsum = 0
  for key,val in table.get(past).items():
    rsum += val
    #print "(key,val): (" + str(key) + "," + str(val) + ")"
    #print "is %f < %f?" % (r, rsum)
    if (r < rsum):
      #print "return " + str(key)
      return key
  #give up and return the last one
  return table.items().pop()

bwintervals = {
0:{0:.5, 1:.2, 2:2., 3:.1, 4:1.5, 5:1. , 6:.1 , 7:.5, 8:.1, 9:.5, 10:.1, 11:.5},
1:{0:.2, 1:.5, 2:.2, 3:2., 4:1. , 5:.1 , 6:1.5, 7:.1, 8:1., 9:.1, 10:1., 11:.1},
2:{0:2., 1:.2, 2:.5, 3:.2, 4:2. , 5:1.5, 6:.1,  7:1., 8:.1, 9:.5, 10:.1, 11:.1},
3:{0:.1, 1:2., 2:.2, 3:.5, 4:.2 , 5:.1 , 6:1.5, 7:.1, 8:1., 9:.1, 10:.5, 11:.1},
4:{0:1.5, 1:.1, 2:2., 3:.2, 4:.5, 5:2., 6:.2, 7:1.5, 8:.1, 9:1., 10:.1, 11:.5},
5:{0:1., 1:.1, 2:1.5, 3:.2, 4:2., 5:.5, 6:.2, 7:2., 8:.1, 9:1.5, 10:.1, 11:1.},
6:{0:.1, 1:1.5, 2:.1, 3:2., 4:.1, 5:.2, 6:.5, 7:.2, 8:2., 9:.1, 10:1.5, 11:.1},
7:{0:.5, 1:.1, 2:1., 3:.1, 4:1.5, 5:2., 6:.2, 7:.5, 8:.2, 9:2., 10:.1, 11:1.5},
8:{0:.1, 1:1., 2:.1, 3:1.5, 4:.1, 5:.1, 6:2., 7:.2, 8:.5, 9:.2, 10:2., 11:.1},
9:{0:.5, 1:.1, 2:.4, 3:.1, 4:1., 5:1.5, 6:.1, 7:2., 8:.2, 9:.5, 10:.2, 11:2.},
10:{0:.1, 1:.5, 2:.1, 3:1., 4:.1, 5:.1, 6:1.5, 7:.1, 8:2., 9:.2, 10:.5, 11:.2},
11:{0:.5, 1:.1, 2:.5, 3:.1, 4:.5, 5:1., 6:.1, 7:1.5, 8:.1, 9:2., 10:.2, 11:.5},
}

bwoctaves = {
'c3':{'c3':2, 'c4':1, 'c5':.5, 'c6':.25},
'c4':{'c3':1, 'c4':2, 'c5': 1, 'c6':.5 },
'c5':{'c3':.5, 'c4':1, 'c5':2, 'c6':1},
'c6':{'c3':.25, 'c4':.5, 'c5':1, 'c6':2}
}


def bw(length, octave, rate):
  ints = bwintervals
  octs = bwoctaves
  reps = 0
  intt = 0
  timepoint = 0
  dur = rate*1.5
  for i in range(length):
    if reps == 0:
      reps = random.choice([4,8,12,16])
      octave = random.choice(octs)
    intt = random.choice(ints)
    STRUM2(timepoint, dur, 10000, keynumToHertz(octave + intt), 1, 1.0, 0.5)
    timepoint += rate
    reps -= 1
    


  
random.seed(1)
#markovRhythms(100, .4, rhydict)
#markovRhythms(100, .4, rhydict2)
#markovRhythms(100, .4, rhydict3)
#markovChorder(25, intmix,  60, 6, .6, 1.2, 1.2, 1)
markovChorder(25, intmix2, 60, 6, .6, .6, 1, 4)

