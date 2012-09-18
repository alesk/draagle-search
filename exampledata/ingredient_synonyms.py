#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection
import codecs

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'draagle'

db = Connection(HOST, PORT)[DATABASE]

def export():
  """
  Finds all synonyms for ingredient and writes them to ingredient_synonyms.txt
  """

  all_synonyms = []
  for ingredient in db.drug_ingredient.find():
    synonyms = set(
        [ingredient.get('name')] + 
        ingredient.get('synonymes', []) +
        ingredient.get('variants', [])
        )
    synonyms_to_merge = filter(lambda s: s.intersection(synonyms), all_synonyms)
    if len(synonyms_to_merge):
      synonyms_to_merge = synonyms.union(synonyms)
    else:
      all_synonyms.append(synonyms)



  with codecs.open("ingredient_synonyms.txt", 'w+', 'utf-8') as fl:
    for synonyms_line in sorted([ ", ".join(s) for s in all_synonyms if len(s) > 1]):
      fl.write("%s\n" % synonyms_line);


if __name__ == "__main__":
  export()
