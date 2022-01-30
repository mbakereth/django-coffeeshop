#!/bin/bash

systemctl status elasticsearch.service

curl -X GET "localhost:9200/?pretty"
{
  "name" : "debian",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "VZHcuTUqSsKO1ryHqMDWsg",
  "version" : {
    "number" : "7.10.1",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "1c34507e66d7db1211f66f3513706fdf548736aa",
    "build_date" : "2020-12-05T01:00:33.671820Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  “tagline”: “You Know, for Search”
}
