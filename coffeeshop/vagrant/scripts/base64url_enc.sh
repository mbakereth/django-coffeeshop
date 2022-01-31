#!/bin/bash

base64 $* | tr '/+' '_-' | tr -d '='
