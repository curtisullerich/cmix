from rtcmix import *
from metalib import *
import math
import random
#print_off()
rtsetparams(44100, 2)
load("STRUM2")

"""
from Chapter 19 (Markov Processes) of Notes from the Metalevel

I chose to represent transition tables as matrices (2D arrays)
where the entry at table[2][3] is the probability of transition
from state 2 to state 3.
"""

#index values for each row/column in the table.
q = 0 #quarter note
e = 1 #eighth note
ed = 2 #dotted eighth
s = 3 #sixteenth
w = 4 #wait (stop and return)
rhydict = dict(q=dict(q=.5,e=2,ed=.75),e=dict(e=3,q=1),ed=dict(s=1),s=dict(e=2,q=1))
rhydict2 = dict(q=dict(q=.5,e=2,ed=.75,w=.2),e=dict(e=3,q=1),ed=dict(s=1),s=dict(e=2,q=1),w=dict(stop=1))
intmix = [[0,0,.4,.4,0.1],[0,.2,.4,.4,.1],[.2,.6,0,.4,0],[0,.2,.4,.4,0],[0,.4,.2,.2,0]]

#Uses markov chains to generate rhythms for a drunk sequence of notes
#Use rhytable  for the first exercise from Metalevel
#and rhytable2 for the second exercise. This function works for both.
def markovRhythms(length, quarterNote):
  tbl = rhydict2
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

def markovChorder(length, intmix, note, size, ud, rhy, dur):
  intt = 1
  key = note
  chord = False
  timepoint = 0
  for i in range(length):
    intt = selectNext(intmix, intt)
    if (random.random() < ud):
      key += indexToChordInt(intt)
      if (key > 90):
        key = 90
    else:
      key -= indexToChordInt(intt)
      if (key < 50):
        key = 50
    chord = []
    for i in range(size):
      n = key
      intt = selectNext(intmix, intt)
      n = n - indexToChordInt(intt)
      chord.append(n)    
    for c in chord:
      STRUM2(timepoint, dur, 10000, keynumToHertz(c), 1, 1.0, 0.5)    
    timepoint += rhy


def indexToChordInt(intt):
  if (intt <= 3):
    return intt + 1
  else:
    return intt + 2

#select the next element of the markov transition table
#given the past value
def selectNext(table, past):
  r = random.uniform(0, sum(table[past]))
  #print "row: " + str(table[past]) 
  #print "sum: " + str(sum(table[past]))
  #print "past: " + str(past)
  #print "r: " + str(r)
  rsum = 0
  for i in range(len(table[past])):
    rsum += table[past][i]
    #print "curval=" + str(table[past][i])
    #print "is %f < %f?" % (r, rsum)
    if (r < rsum):
      return i
  #give up and return the last one
  return len(table[past]) - 1

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
  
  
random.seed(3)
markovRhythms(100, .4)
#markovChorder(25, intmix, 60, 6, .6, 1.2, 1.2)

