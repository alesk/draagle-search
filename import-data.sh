#!/bin/sh

# http://wiki.apache.org/solr/UpdateJSON
curl "http://localhost:8983/solr/draagle/update/json?commit=true" -H "Content-Type: text/plain; charset=utf-8" --data-binary @exampledata/drugs.json
