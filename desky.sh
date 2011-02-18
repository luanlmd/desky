#! /bin/bash
THEME=$1
if [ -z "$THEME" ]
then
	THEME="default"
fi   
python $THEME/desky.py
