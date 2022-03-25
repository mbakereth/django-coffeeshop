#!/bin/bash

mkdir -p /run/kibana
chown kibana.kibana /run/kibana

systemctl enable elasticsearch.service
systemctl start elasticsearch.service

systemctl enable logstash.service
systemctl start logstash.service

systemctl enable kibana.service
systemctl start kibana.service

