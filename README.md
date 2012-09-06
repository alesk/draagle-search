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



## Misc notes

I screwed up adding `sorl-home/draagle/data` to index and commited. The rollback included:

    git reset --soft "HEAD^"
    git rm -r --cache solr-home/draagle/data
  

