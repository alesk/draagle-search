#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection, ASCENDING
from string import lower
import codecs

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'draagle'

db = Connection(HOST, PORT)[DATABASE]
INGREDIENT=10

def export():
  """
  Finds all synonyms for ingredient and writes them to ingredient_synonyms.txt
  """

  all_synonyms = []
  indications = set()
  for fact in db.drug_fact.find({'sort':INGREDIENT}):
    indications.add(lower(fact['name']))

  with codecs.open('indication_synonyms.txt', 'w', 'utf-8') as fl:
    fl.write("\n".join(sorted(indications)))
    fl.close()

if __name__ == "__main__":
  export()
