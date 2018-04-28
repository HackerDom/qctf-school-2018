#!/bin/bash

./gen.py \
    --seed "longjump" \
    --mask "QCTF{w0w_reD1r3cts_%s}" \
    --count 1000 \
    --length 5 \
    --pretty \
> teams.py
