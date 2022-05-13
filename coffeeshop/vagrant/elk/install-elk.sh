#!/bin/bash

# From examples in the following URLs:
# https://linuxhint.com/visualize_apache_logs_with_elk_stack/
# https://www.elastic.co/guide/en/elasticsearch/reference/7.16/deb.html#deb-repo
# https://www.elastic.co/guide/en/logstash/current/config-examples.html

. /secrets/config.env

export DEBIAN_FRONTEND=noninteractive

cd /root

# install Elasticsearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
apt-get update
apt-get install elasticsearch
/bin/systemctl daemon-reload
/bin/systemctl enable elasticsearch.service
systemctl start elasticsearch.service

# install Logstash
apt-get install logstash
adduser logstash adm

# install Kibana
apt-get install kibana

# Configure Elasticsearch
# this reduces the number of shards as the default number for production is higher 
# than we need for development
(cd /vagrant/elk ; curl -X PUT http://localhost:9200/_template/defaults -H 'Content-Type:application/json' -d @index_template.json)

# Add reporting config to read Apache log files
cp /vagrant/elk/apache.conf /etc/logstash/conf.d/apache.conf

# Start logstash
systemctl enable logstash.service
systemctl restart logstash.service

# Configure Kibana
# Bind to address 0.0.0.0 so we can access it from outside
# WARNING: we are not configuring any authentication.  In a productive
# environment we would have to do that, or restrict who can access the
# host/port
echo 'server.host: "0.0.0.0"' >> /etc/kibana/kibana.yml

# Start kibana
sudo systemctl enable kibana.service && sudo systemctl restart kibana.service

# There seems to be an intermittent bug in logrotate preventing Apache from rotating logs propery.  This should fix it
invoke-rc.d apache rotate >/dev/null 2>&1
service apache2 restart

