#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection
from string import strip
import codecs
import json

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'draagle'

db = Connection(HOST, PORT)[DATABASE]

INGREDIENT = 30

def filter_by_sort(coll, sort):
  return filter(lambda x:x['sort'] == sort, coll)

def populate_drug(drug, files):
    drug_id = drug['_id']
    atc_id = drug['atc']
    atc_name = None

    if atc_id:
      atc = db.drug_atc.find_one({'$or':[{'_id':atc_id}, {'name':atc_id}]})
      atc_name = strip("%s %s" % (atc_id, atc.get('name', '')))
      files['atc'].append({
        'type':'atc', 
        'id':atc_id,
        'name': atc_name
        })

    facts = list(db.drug_fact.find({'drugs':drug_id}))

    ingredient_ids = [ f['ingredients'] for f in filter_by_sort(facts, INGREDIENT)]
    ingredients = list(db.drug_ingredient.find({'_id':{'$in':ingredient_ids}}))

    for i in ingredients:
      files['ingredients'].append({
        'type':'ingredient', 
        'id':i['_id'],
        'name':i['name']
        })

    files['drugs'].append({
      'type':'drug', 
      'id':'drug',
      'name':drug['name'],
      'atc': atc_name,
      'ingredients':sum([ i.get('known_as', [i.get('name')]) for i in ingredients], [])
      })


def populate():

  files = {
    'atc':[],
    'ingredients':[],
    'drugs':[],
    'indications':[],
    'parties':[]
  }

  index = 0
  for drug in db.drug_drug.find({'is_proxy':False}):
    index += 1
    if not index % 5 == 0:
      continue
    populate_drug(drug, files)

  return files

def export():

  files = populate()

  for file_name, objects in files.items():
    with codecs.open("%s.json" %file_name, 'w+', 'utf-8') as fl:
      fl.write("[\n");
      fl.write("\n,".join([json.dumps(o) for o in objects]))
      fl.write("]\n");


if __name__ == "__main__":
  export()
