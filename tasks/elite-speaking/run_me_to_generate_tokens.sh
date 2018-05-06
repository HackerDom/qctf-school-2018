#!/bin/bash

./token_generator.py \
    --seed "elitespeaking" \
    --mask "QCTF{w0w_5o_ea5y_2_r34d_%s}" \
    --count 500 \
    --length 6 \
    --pretty \
> tokens.py
