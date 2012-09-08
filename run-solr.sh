#!/bin/sh
echo "Running Solr AutoComplete example in Jetty."
echo "Syntax: ./run-solr.sh [<port>]"

if [ X$JETTY_HOME = X ] ; then
	echo "Please set environment variable JETTY_HOME to point to your Solr example directory"
	echo "Example: export JETTY_HOME=/Users/ales/3rd/solr-4.0.0/solr/example"
	exit
fi	
if [ X$1 != X ] ; then
  PORT=$1
else
  PORT=8983
fi

SOLR_HOME=`pwd`/solr-home

export JAVA_OPTIONS="-server \
                     -XX:+UseConcMarkSweepGC \
                     -XX:+CMSClassUnloadingEnabled \
                     -XX:-CMSParallelRemarkEnabled \
                     -XX:+UseCMSCompactAtFullCollection \
                     -XX:+UseParNewGC \
                     -XX:+PrintGCDetails \
                     -Xms512m -Xmx1024m \
                     -Duser.language=sl \
                     -Duser.country=SI \
                     -Dsolr.solr.home=$SOLR_HOME \
                     -Djetty.port=$PORT \
                     $JAVA_OPTIONS"
echo JAVA_OPTIONS is $JAVA_OPTIONS

cd $JETTY_HOME
java $JAVA_OPTIONS -jar start.jar

