#!/usr/bin/env python

# Computation of Levenshtein distance
# Levenshtain distance is the number of required changes between strings 
# to make them equal

from memoized import memoized

@memoized
def distance(s, t):
  """
  >>> distance("mocna bolecina", "mocne bolecine")
  2
  """
  len_s = len(s)
  len_t = len(t)

  if len_s == 0:
    return len_t
  if len_t == 0:
    return len_s

  cost = 1 if s[0] != t[0] else 0  
  
  c = (
      distance(s[1:len_s - 1], t) + 1,
      distance(s, t[1:len_t - 1]) + 1,
      distance(s[1:len_s], t[1:len_t]) + cost)

  return min(*c)

