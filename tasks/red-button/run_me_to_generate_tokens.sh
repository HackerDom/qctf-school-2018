#!/bin/bash

./token_generator.py \
    --seed "redbutton" \
    --mask "QCTF{bo0oO0o0Oo0Om_%s}" \
    --count 1000 \
    --length 5 \
    --pretty \
> tokens.py
