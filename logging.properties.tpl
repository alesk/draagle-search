#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# To use this log config, start solr with the following system property: 
# -Djava.util.logging.config.file=etc/logging.properties

## Default global logging level:
.level = WARNING

## Log every update command (add, delete, commit, ...)
#org.apache.solr.update.processor.LogUpdateProcessor.level = FINE

## Where to log (space separated list).
handlers = java.util.logging.FileHandler, java.util.logging.ConsoleHandler

# levels for certain handlers
java.util.logging.ConsoleHandler.level = WARNING
java.util.logging.FileHandler.level = FINE

# write log messages in human readable format
java.util.logging.ConsoleHandler.formatter = java.util.logging.SimpleFormatter
java.util.logging.FileHandler.formatter = java.util.logging.SimpleFormatter

# cca 1 MB limit per file, 10 files
java.util.logging.FileHandler.limit = 1000000
java.util.logging.FileHandler.append = true
java.util.logging.FileHandler.count = 10


# Log to the logs directory, with log files named solrxxx.log
# java.util.logging.FileHandler.pattern = ${solr.solr.home}/../logs/solr%u.log
java.util.logging.FileHandler.pattern = /home/draagle2/draagle-search/logs/solr%u.log
