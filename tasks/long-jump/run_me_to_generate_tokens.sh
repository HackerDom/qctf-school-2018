#!/bin/bash

./token_generator.py \
    --seed "longjump" \
    --mask "QCTF{go0dr3d1reC7s_%s}" \
    --count 1000 \
    --length 5 \
    --pretty \
> tokens.py
