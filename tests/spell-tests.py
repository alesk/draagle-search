from urllib2 import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

URL="http://localhost:8983/solr/draagle/select?q=%s&wt=python"
def runQuery(query):
  conn = urlopen(URL % query)
  return eval(conn.read())

def test_aspirn():
  response = runQuery("aspirn+tbleta")
  suggestions = response['spellcheck']['suggestions']
  
  assert suggestions[0] == 'aspirn'
  assert 'aspirin' in suggestions[1]['suggestion']

  assert suggestions[2] == 'tbleta'
  assert 'tableta' in suggestions[3]['suggestion']
  #pp.pprint(response)


if __name__ == "__main__":
  test_aspirn()
