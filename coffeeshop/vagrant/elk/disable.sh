#!/bin/bash

systemctl disable kibana.service
systemctl stop kibana.service

systemctl disable logstash.service
systemctl stop logstash.service

systemctl disable elasticsearch.service
systemctl stop elasticsearch.service

