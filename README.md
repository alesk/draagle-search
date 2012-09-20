draagle-search
==============

Configuration of solr search for draagle.com

## run

Use `source env` or set `JETTY_HOME` by hand. `JETTY_HOME` should point to examples directory
of solr instalation, such as:

    export JETTY_HOME=/Users/ales/3rd/solr-4.0.0/solr/example

Why? http://stackoverflow.com/questions/496702/can-a-shell-script-set-environment-variables-of-the-calling-shell

## query

Openup browser and type in the address bar to get all Aspirins:

    http://localhost:8983/solr/draagle/ac?q=Asp*

## Deploying solr

For logging, copy `logging.properties` to `$SOLR_HOME` and append 

    `-Djava.util.logging.config.file=logging.properties`

to `$JAVA_OPTIONS` in `run-solr.sh`.

## Faceting

Faceting works best when data is untokenized. I us special field `ingredients_facet` for this
purpose. It uses plain solr `string` type without tokenisation and storing.

See: http://wiki.apache.org/solr/SolrFacetingOverview

## Misc notes

### git commit ups
I screwed up adding `sorl-home/draagle/data` to index and commited. The rollback included:

    git reset --soft "HEAD^"
    git rm -r --cache solr-home/draagle/data

### including child documents
I tried to use xinclude to compose config files out of fragments, but of no luck. The problem was
invoking more than one node from the child document. At the end, I used SGML entities as
proposed by Bogdan Nicolau in:

http://lucene.472066.n3.nabble.com/XInclude-Multiple-Elements-td3167658.html

### Unit tests with plovr

For testing with plovr see http://plovr.com/testing.html.

## Research directions

  * payloads http://sujitpal.blogspot.com/2010/10/denormalizing-maps-with-lucene-payloads.html  


## References

  1 https://github.com/cominvent/autocomplete
  2 "IBM's series on solr" http://www.ibm.com/developerworks/java/library/j-solr1/#searching
