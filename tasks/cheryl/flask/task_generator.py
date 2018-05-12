from calendar import month_abbr
from random import shuffle

MONTHES = list(month_abbr)[1:]
DAYS = list(range(1,29))
good = [
    [0,1,1,0,0,1],
    [0,0,0,1,1,0],
    [1,0,1,0,0,0],
    [1,1,0,1,0,0]
]

def generate():
    shuffle(MONTHES)
    shuffle(DAYS)

    monthes, days = MONTHES[:4], DAYS[:6]
    answer = '{} {}'.format(days[2], monthes[2])

    res = []
    for x in range(4):
        for y in range(6):
            if good[x][y]:
                res.append('{} {}'.format(days[y], monthes[x]))

    shuffle(res)
    return answer, res