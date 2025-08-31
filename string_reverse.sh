#!/bin/bash

echo "Enter String to reverse"
read str

rev=""

len=$(#str)

for ( i=$len-1; i>=0; i--); do
    rev="$rev$(str:$i:1)"
done

echo "Orginal String $str"
echo "Reverese String $rev"

