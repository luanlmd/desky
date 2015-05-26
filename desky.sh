#! /bin/bash

MYPATH="${0%/*}"
THEME=$1
if [ -z "$THEME" ]
then
	THEME="default"
fi   
python2 $MYPATH/$THEME/desky.py
