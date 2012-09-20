#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from pymongo import Connection
from string import strip
from hashlib import md5
import urllib, urllib2
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

def drug_to_solr(drug_id):
    drug = db.drug_drug.find_one(drug_id)
    drug_id = drug['_id']
    atc_id = drug['atc']
    atc_name = None

    if atc_id:
      atc = db.drug_atc.find_one({'$or':[{'_id':atc_id}, {'name':atc_id}]})
      atc_name = strip("%s %s" % (atc_id, atc.get('name', '')))
      yield {
        'type':'atc', 
        'id':atc_id,
        'name': atc_name
        }

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
        yield {
          'type':'ingredient', 
          'id':md5(name.encode('utf-8')).hexdigest(),
          'name':name
          }

    for name in indications:
      yield {
        'type':'indication', 
        'id':md5(name.encode('utf-8')).hexdigest(),
        'name':name }

    if manufacturer:
      yield {
        'type':'manufacturer', 
        'id':md5(manufacturer.encode('utf-8')).hexdigest(),
        'name':manufacturer }

    if idzp:
      yield {
        'type':'idzp', 
        'id':md5(idzp.encode('utf-8')).hexdigest(),
        'name':idzp }

    yield {
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
      }
    
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

def get_drug_proxy_list(criteria = {}):
    return [ (d['_id'], d['name']) for d in 
        db.drug_drug.find(criteria, fields=('_id', 'name')) ]

def report_solr_error(response_json):
  response = json.loads(response_json)
  print response['responseHeader']

def solr_import():
  WANTED_TYPES=['ingredient', 'drug']

  for drug_id, drug_name in get_drug_proxy_list():
    break
    print drug_id, drug_name
    docs = filter(lambda x: x['type'] in WANTED_TYPES, drug_to_solr(drug_id))
    json_to_send = "[%s]" % ",\n".join([json.dumps(doc) for doc in docs])
    report_solr_error(solr_send(json_to_send, options={'commit':'true'}))

  report_solr_error(solr_send(None, options={'optimize':'true', 'wt':'json'}))

    
UPDATE_URL="http://localhost:8983/solr/draagle/update/json"
def solr_send(payload, options={}):
  url = "%s?%s" % (UPDATE_URL, urllib.urlencode(options))
  print url
  if payload:
    solrReq = urllib2.Request(url, payload)
  else:
    solrReq = urllib2.Request(url)

  solrReq.add_header("Content-Type", "text/json; charset=utf-8")
  solrPoster = urllib2.urlopen(solrReq)
  response = solrPoster.read()
  solrPoster.close()
  return response


if __name__ == "__main__":
  #export()
  solr_import()
