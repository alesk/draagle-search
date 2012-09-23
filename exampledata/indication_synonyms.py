#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection, ASCENDING
from string import lower
import levenshtein
import codecs
from hashlib import md5
from string import strip
import sys

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'draagle'

db = Connection(HOST, PORT)[DATABASE]
INGREDIENT=10

def get_indications():
  for fact in db.drug_fact.find({'sort':INGREDIENT}).sort([('name', ASCENDING)]):
    yield fact['name']


def export():
  """
  Finds all synonyms for ingredient and writes them to ingredient_synonyms.txt
  """

  all_synonyms = []
  indications = set()
  for name in get_indications():
    indications.add(lower(fact['name']))

  with codecs.open('indication_synonyms.txt', 'w', 'utf-8') as fl:
    fl.write("\n".join(sorted(indications)))
    fl.close()


def is_similar_levenshtein(s, t):
  words_s = s.split()
  words_t = t.split()
  len_s = len(words_s)
  len_t = len(words_t)

  if s == t: return False
  if len_s != len_t: return False
  similarity = sum([ levenshtein.distance(words_s[i], words_t[i]) for i in range(len_s) ])
  if sum == 0 or sum > len_s*2: return False
  return True

def stemize(s):
  """
  >>> stemize("pljucnih bolezni")
  'pljucn bolezn'
  >>> stemize("pri pljucnih za boleznimi")
  'pr pljucn z boleznim'
  """
  lower_s = s.lower()
  last_vocal = lambda x: max([i for i, c in enumerate(x) 
      if c in ['a', 'e', 'i', 'o', 'u']] or [len(x)])
  return " ".join([ strip(w[0: len(w) > 3 and last_vocal(w) or len(w)]) for w in s.split() if strip(w)])

def get_condensed_indications(file_name):
  with codecs.open(file_name, 'r', 'utf-8') as fl:
    return [ strip(line) for line in fl.readlines() if strip(line)]

def condense(condensed_indications):

  ci = get_condensed_indications(condensed_indications)
  stemized_ci = list(enumerate([ stemize(c) for c in ci]))
  lines = []
  for indication in sorted(set(get_indications())):
    stem = stemize(indication)
    condensed = set()
    for idx, s in stemized_ci:
      f = stem.find(s)
      if f > 0 and stem[f-1] == ' ' or f == 0:
        condensed.add(ci[idx])

    if condensed:
      line = "%s => %s" %(indication, max(condensed))
      lines.append(line)
    #else:
    #  line = "%s => **EMPTY**" % indication

  with codecs.open('groupped_indications.txt', 'w+', 'utf-8') as fl:
       fl.write("%s\n" % "\n".join(lines))



if __name__ == "__main__":
  # export()
  condense(sys.argv[1])
