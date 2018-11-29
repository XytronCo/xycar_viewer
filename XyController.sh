#!/bin/bash

a=""
while [ True ]; do
a=$(echo `ps -ef | grep "zeitgeist-fts" | grep -v "grep"` | cut -d " " -f2)
if [ "$a" = "" ]; then
continue
else
cd ~/Desktop/XyController/
python3 ./XyController.py
break
fi
done
