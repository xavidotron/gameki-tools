#!/bin/bash

set -e

pages="$(/opt/local/bin/pdfinfo "$1" | awk '/Pages/ {print $2}')"

needed="$(bc <<< "3 - $pages % 4")"

echo "Pages: $pages; needed: $needed"

sel="-"
for (( i = 0 ; i<$needed; i=i+1 )) ; do
    sel="{},$sel"
done

pdfbook --short-edge --paper letter -o "$3" "$1" - "$2" "$sel"
