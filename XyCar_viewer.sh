#!/bin/bash

a=""
b=$(echo `pwd | grep "xycar_viewer" | grep -v "grep"`)
if [ "$b" = "" ]; then
echo "자신의 경로에서만 실행할 수 있습니다."
exit
else
export Xycar_path=`pwd`
fi
while [ True ]; do
a=$(echo `ps -ef | grep "zeitgeist-fts" | grep -v "grep"` | cut -d " " -f2)
if [ "$a" = "" ]; then
continue
else
pwd
cd $Xycar_path/
python3 ./XyCar_viewer.py
break
fi
done
