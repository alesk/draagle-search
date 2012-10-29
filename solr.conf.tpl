description "Solr Search Server"

env JETTY_PORT=8983
env JETTY_HOME=/home/draagle2/solr
env SOLR_HOME=/home/draagle2/draagle-search/solr-home
env JAVA_OPTIONS="-server \
		  -XX:+UseConcMarkSweepGC \
		  -XX:+CMSClassUnloadingEnabled \
		  -XX:-CMSParallelRemarkEnabled \
		  -XX:+UseCMSCompactAtFullCollection \
		  -XX:+UseParNewGC \
		  -Xms128m -Xmx400m \
		  -Duser.language=sl \
		  -Duser.country=SI"
export SOLR_HOME
export JETTY_HOME

# Make sure the file system and network devices have started before
# we begin the daemon
start on (filesystem and net-device-up IFACE!=lo)

# Stop the event daemon on system shutdown
stop on shutdown

# Respawn the process on unexpected termination
respawn

# put all output to /var/log/upstart/solr.log
#console log


# The meat and potatoes
#exec /usr/bin/java -Xms128m -Xmx256m -Dsolr.solr.home=/path/to/solr/home -Djetty.home=/path/to/jetty -jar /path/to/jetty/start.jar >> /var/log/solr.log 2>&1

exec /usr/local/bin/java $JAVA_OPTIONS \
    -Dsolr.solr.home=$SOLR_HOME \
    -Djetty.home=$JETTY_HOME \
    -Djetty.port=$JETTY_PORT \
    -Djava.util.logging.config.file="$SOLR_HOME/../logging.properties" \
    -jar $JETTY_HOME/start.jar >> /var/log/solr.log 2>&1
