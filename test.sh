#!/bin/bash
x=$(echo "$1" | ./Parser/pparser)
python3 main.py $x