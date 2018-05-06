#!/bin/bash

./token_generator.py \
    --seed "oldfriend" \
    --mask "QCTF{3_PX_WIDE_CHARS_%s}" \
    --count 1000 \
    --length 4 \
    --pretty \
    --alpha "0123456789QCTFPXIDHAR" \
> tokens.py
