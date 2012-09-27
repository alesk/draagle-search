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


def stem_word(word, stem_exceptions={}):
  last_vocal = lambda x: max([i for i, c in enumerate(x) 
      if c in ['a', 'e', 'i', 'o', 'u']] or [len(x)])


  if word in stem_exceptions.keys():
    return stem_exceptions[word]
  elif len(word) < 4:
    return word
  else:
    return word[0: last_vocal(word)]

def stemize(s, stem_exceptions={}):
  """
  >>> stemize("pljucnih bolezni")
  'pljucn bolezn'
  >>> stemize("pri pljucnih za boleznimi")
  'pr pljucn z boleznim'
  """
  lower_s = s.lower()
  
  return " ".join([ stem_word(strip(w), stem_exceptions) for w in s.split() if strip(w)])

def get_condensed_indications(file_name):
  with codecs.open(file_name, 'r', 'utf-8') as fl:
    return [ strip(line) for line in fl.readlines() if strip(line)]


def get_stem_exceptions(file_name):
  """
  Each line must include two words. 1st word is transformed to 2nd.
  """
  with codecs.open(file_name, 'r', 'utf-8') as fl:
    return [ map(strip, filter(strip, line.split(' '))) for line in fl.readlines() if strip(line)]

def get_condense_exceptions(file_name):
  """akne brazgotine
     means 'akne' would be choosen over 'brazgotine' despite of 'brazgotine' is longer
  """ 
  
  with codecs.open('condense_exceptions.txt', 'r', 'utf-8') as fl:
    return [ filter(strip, line.split(' ')) for line in fl.readlines() if strip(line)]

def condense_phrase(stemed_phrase, condensed_indications, stemized_ci):
    condensed = set()
    stemed_phrase_set = set(stemed_phrase.split(' '))
    for idx, s in enumerate(stemized_ci):
      if stemed_phrase_set.intersection(s) == s:
        condensed.add(condensed_indications[idx])

    return condensed

def condense(options):

  processed_options = process_options(options)
  stem_exceptions = processed_options.get('stem_exceptions')
  condensed_indications = processed_options.get('condensed_indications')
  stemized_ci = processed_options.get('stemized_ci')

  lines = []

  for indication in sorted(set(get_indications())):
      stemized_indication = stemize(indication, stem_exceptions)
      condensed_set = condense_phrase(stemized_indication, condensed_indications, stemized_ci)
      line = "%s => %s" %(indication, "; ".join(condensed_set))
      lines.append(line)
    #else:
    #  line = "%s => **EMPTY**" % indication

  with codecs.open('groupped_indications2.txt', 'w+', 'utf-8') as fl:
       fl.write("%s\n" % "\n".join(lines))

def process_options(options):
  """
  return state file with all special lists included
  """
  stem_exceptions_name = options.get('stem_exceptions', None)
  condensed_indications_name = options.get('condensed_indications', None)
  condensed_indications = condensed_indications_name and get_condensed_indications(condensed_indications_name)
  stem_exceptions = dict(stem_exceptions_name and get_stem_exceptions(stem_exceptions_name))
 

  return dict(
      stem_exceptions = stem_exceptions, 
      condensed_indications = condensed_indications,
      stemized_ci = [ set(stemize(c, stem_exceptions).split(' ')) for c in condensed_indications]
  )

def debug(phrase, options):
  processed_options = process_options(options)

  stem = stemize(phrase, processed_options.get('stem_exceptions'))
  condensed = condense_phrase(stem, processed_options.get('condensed_indications'), processed_options.get('stemized_ci'))
  print "%s         " % phrase
  print "  stem:      %s" % stem
  print "  condensed: %s" % ", ".join(condensed)

if __name__ == "__main__":
  options = dict(
      stem_exceptions='stem_exceptions.txt', 
      condensed_indications='indication.txt')
  # export()  
  condense(options)

  # test
  #a = u"anemija zaradi zvečane izgube železa, zaradi krvavitev iz peptičnega ulkusa => zvin, anemija zaradi zvečane izgube železa" 

  #a = u"akutna limfoblastna levkemija"
  #debug(a, options)
