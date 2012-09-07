#!/bin/sh

# http://wiki.apache.org/solr/UpdateJSON
for file in atc.json ingredients.json drugs.json; do
  curl "http://localhost:8983/solr/draagle/update/json?commit=true" \
    -H "Content-Type: text/plain; charset=utf-8" \
    --data-binary @exampledata/$file
done
