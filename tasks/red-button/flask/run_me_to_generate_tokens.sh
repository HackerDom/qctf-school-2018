#!/bin/bash

./token_generator.py \
    --seed "redbutton" \
    --mask "QCTF{bo0Om_%s}" \
    --count 500 \
    --length 4 \
    --pretty \
> tokens.py
