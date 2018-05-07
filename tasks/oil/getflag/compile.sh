#!/bin/bash

./generate.py --template getflag.c.template --tokens tokens --output getflag.c

gcc getflag.c -o getflag
