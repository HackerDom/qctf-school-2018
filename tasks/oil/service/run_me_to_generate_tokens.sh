#!/bin/bash

./token_generator.py \
    --seed "oil" \
    --mask "QCTF{w0w_y0u_h4ck3D_my_Oil_%s}" \
    --count 500 \
    --length 8 \
    --pretty \
> tokens.py
