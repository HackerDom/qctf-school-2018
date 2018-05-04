#!/bin/bash

./token_generator.py \
    --seed "anomaly" \
    --mask "QCTF{h34r7h3d1ff3r3nc3_%s}" \
    --count 1000 \
    --length 8 \
    --pretty \
    --alpha "0123456789" \
> tokens.py
