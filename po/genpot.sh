#!/bin/bash
POTFILE="new/toast-machine.pot"
if ! [ -d new ]
then
  mkdir new
fi

if [ -f ../data/ui/*.glade.h ]
then
  rm ../data/ui/*.glade.h
fi
intltool-extract --type=gettext/glade ../data/ui/toast-machine.glade
intltool-extract --type=gettext/glade ../data/ui/toast-machine-conf.glade

if ! [ -f $POTFILE ]
then
  touch $POTFILE
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output $POTFILE ../data/ui/*.glade.h ../src/*.py
rm ../data/ui/*.glade.h
read
