#!/bin/bash

./token_generator.py \
    --seed "blindrobot" \
    --mask "QCTF{m1gh7_b3_th3_loo0ng35t_fLag_y0u_hav3_Ever_s33N_%s}" \
    --count 500 \
    --length 5 \
    --pretty \
> tokens.py
