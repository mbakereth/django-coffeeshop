#!/bin/bash

inp=$(</dev/stdin)
len=$(echo -n $inp | wc -c)
while [ $(expr $len % 4) != 0 ]; do
	inp=$(echo -n "${inp}=")
	len=$(echo -n $inp | wc -c)
done
echo -n $inp | tr '_-' '/+' | base64 -d
