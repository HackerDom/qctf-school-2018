#!/bin/bash

./token_generator.py \
    --seed "brokentransmitter" \
    --mask "QCTF{c0ngra7ulat10ns_y0u_c4n_hacK_eld3r_traN5m1tt3rs_%s}" \
    --count 500 \
    --length 10 \
    --pretty \
> tokens.py
