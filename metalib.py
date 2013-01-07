import math

def rescale(x, oldmin, oldmax, newmin, newmax):
  oldrange = oldmax - oldmin
  newrange = newmax - newmin
  oldsize  = x - oldmin
  return ((newrange/oldrange) * oldsize) + newmin

def keynumToHertz(keynum):
  lowestfreq = 8.175 #C-1
  return lowestfreq * math.pow(2.0, float(keynum)/12.0)

