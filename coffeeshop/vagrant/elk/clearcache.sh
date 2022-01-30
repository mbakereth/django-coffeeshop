#!/bin/bash

curl -XPOST 'http://localhost:9200/_cache/clear'
curl -XDELETE 'http://localhost:9200/_all'

