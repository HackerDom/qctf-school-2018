#!/bin/bash

gcc -fno-stack-protector -mpreferred-stack-boundary=2 -z execstack -m32 oil.c -o oil &>/dev/null
