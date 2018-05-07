#!/bin/bash

./generate.py --template getflag.c.template --tokens tokens --output getflag.c

gcc -m32 getflag.c -o getflag
