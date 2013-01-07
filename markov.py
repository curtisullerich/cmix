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
rhytable = [[.5, 2, .75, 0], [0, 3, 0, 1], [0, 0, 0, 1], [1, 2, 0, 0]]
rhytable2 = [[.5, 2, .75, 0, .2],[1,3,0,0,0],[0,0,0,1,0],[1,2,0,0,0],[0,0,0,0,1]]
tcurve = [0, 1, .7, .75, 1, 1]

#Uses markov chains to generate rhythms for a drunk sequence of notes
#Use rhytable  for the first exercise from Metalevel
#and rhytable2 for the second exercise. This function works for both.
def markovRhythms(length, quarterNote):
  tbl = rhytable2
  r =  0
  drunk = Drunk(60, 6, 40, 80, 3, 10)
  timepoint = 0
  amp = 10000
  for i in range(length):
    k = drunk.next()
    r = selectNext(tbl, r)
    pulse = quarterNote
    print "r=" + str(r)
    if r is q:
      dur = pulse
    elif r is e:
      dur = pulse/2.
    elif r is ed:
      dur = pulse / 2.
      dur = dur * 1.5
    elif r is s:
      dur = pulse / 4.
    elif r is w:
      return
    STRUM2(timepoint, pulse, amp, keynumToHertz(k), 1, 1.0, 0.5)
    timepoint += dur

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
  
  
  
markovRhythms(100, .4)
