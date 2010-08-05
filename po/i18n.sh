#!/bin/bash
for file in *.po
do
  msgmerge -U $file toast-machine.pot
done

for file in *.po
do (
  if [ -d ${file/.po/} ];
    then rm -r ${file/.po/}
  fi
  mkdir -p ${file/.po/}/LC_MESSAGES
  msgfmt --output-file=${file/.po/}/LC_MESSAGES/toast-machine.mo $file
)
done
read
