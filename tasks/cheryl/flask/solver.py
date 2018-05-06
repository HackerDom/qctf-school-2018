#!/usr/bin/env python3
from collections import Counter

if __name__ == "__main__":
    data = {tuple(x.split()) for x in input().split(', ')}
    bad_dates = dict(y for y in data if y[0] in {x[0] for x in Counter([z[0] for z in data]).items() if x[1] == 1})
    data = {(x,y) for x,y in data if not (x in bad_dates.keys() or y in bad_dates.values())}
    data = {y for y in data if y[0] not in {x[0] for x in Counter(x[0] for x in data).items() if x[1] != 1}}
    res =  {y for y in data if y[1] not in {x[0] for x in Counter(x[1] for x in data).items() if x[1] != 1}}.pop()
    print(' '.join(res))