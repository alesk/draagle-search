draagle-search
==============

Configuration of solr search for draagle.com

## Dependencies
The only dependency is Oracle java. To [install on ubuntu][4], do:

    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java7-installer

## Run

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

## InstallinElasticSearch

If this is your first install, automatically load ElasticSearch on login with:
    mkdir -p ~/Library/LaunchAgents
    ln -nfs /usr/local/Cellar/elasticsearch/0.19.9/homebrew.mxcl.elasticsearch.plist ~/Library/LaunchAgents/
    launchctl load -wF ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist

If this is an upgrade and you already have the homebrew.mxcl.elasticsearch.plist loaded:
    launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist
    ln -nfs /usr/local/Cellar/elasticsearch/0.19.9/homebrew.mxcl.elasticsearch.plist ~/Library/LaunchAgents/
    launchctl load -wF ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist

If upgrading from 0.18 ElasticSearch requires flushing before shutting
down the cluster with no indexing operations happening after flush:
    curl host:9200/_flush

To stop the ElasticSearch daemon:
    launchctl unload -wF ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist

To start ElasticSearch manually:
    elasticsearch -f -D es.config=/usr/local/Cellar/elasticsearch/0.19.9/config/elasticsearch.yml

See the 'elasticsearch.yml' file for configuration options.

You'll find the ElasticSearch log here:
    open /usr/local/var/log/elasticsearch/elasticsearch_ales.log

The folder with cluster data is here:
    open /usr/local/var/elasticsearch/elasticsearch_ales/

You should see ElasticSearch running:
    open http://localhost:9200/
  

## Install solr as service with upstart

Copy `solr.conf.tpl` to `/etc/init/solr.conf` and set paths accordingly. Copy `logging.properties.tpl`
to `logging.properties` in $SOLR_HOME and correct loging path.

You can start solr with:

    sudo start solr

## References

[1]: https://github.com/cominvent/autocomplete
[2]: "IBM's series on solr" http://www.ibm.com/developerworks/java/library/j-solr1/#searching
[3]: http://blog.willcarpenterinteractive.com/2010/07/01/solr-search-stop-words-and-dismax-search-handler/
[4]: http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
