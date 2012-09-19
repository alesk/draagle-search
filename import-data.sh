#!/bin/sh

# http://wiki.apache.org/solr/UpdateJSON
for file in exampledata/*.json; do
  curl "http://localhost:8983/solr/draagle/update/json?commit=true" \
    -H "Content-Type: text/json; charset=utf-8" \
    --data-binary @$file
done
