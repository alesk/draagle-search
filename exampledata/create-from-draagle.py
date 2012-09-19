#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection
from string import strip
from hashlib import md5
import codecs
import json

HOST = '127.0.0.1'
PORT = 27017
DATABASE = 'draagle'

db = Connection(HOST, PORT)[DATABASE]

INDICATION = 10
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
    known_as = dict([ (i['name'], i.get('known_as', [i.get('name')])) 
      for i in ingredients])

    indications = [ f['name'] for f in filter_by_sort(facts, INDICATION) if f['name']]
    manufacturer = drug.get('manufacturer','') or ''
    idzp = drug.get('idzp','') or ''

    for i in ingredients:
      for name in known_as[i['name']]:
        files['ingredients'].append({
          'type':'ingredient', 
          'id':md5(name.encode('utf-8')).hexdigest(),
          'name':name
          })

    for name in indications:
      files['indications'].append({
        'type':'indication', 
        'id':md5(name.encode('utf-8')).hexdigest(),
        'name':name })

    if manufacturer:
      files['parties'].append({
        'type':'manufacturer', 
        'id':md5(manufacturer.encode('utf-8')).hexdigest(),
        'name':manufacturer })

    if idzp:
      files['parties'].append({
        'type':'idzp', 
        'id':md5(idzp.encode('utf-8')).hexdigest(),
        'name':idzp })

    files['drugs'].append({
      'type':'drug', 
      'id':drug['_id'],
      'name':drug['name'],
      'atc': atc_name,
      'identities':[ i for i in drug.get('identities') if len(i or '') > 4],
      'ingredients':[ k for k in known_as.keys()],
      'known_as':sum([v for v in known_as.values()], []),
      'indications':[ f['name'] for f in filter_by_sort(facts, INDICATION) if f['name']],
      'manufacturer':drug['manufacturer'],
      'idzp':drug['idzp'],
      'is_proxy':drug['is_proxy'],
      'rezim_izdaje':drug.get('rezim_izdaje', None),
      'trigonik':drug.get('trigonik', None),
      'product_type':drug.get('product_type', "8")
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
  for drug in db.drug_drug.find():
    index += 1
    #if not index % 3 == 0:
    #  continue
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
