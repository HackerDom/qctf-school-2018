#!/usr/bin/python3

from collections import Counter
import requests
from bs4 import BeautifulSoup

HOST = "https://cheryl.contest.qctf.ru/"
USERNAME = "***"
PASSWORD = "***"

def filter_data(data):
    data = {tuple(x.split()) for x in data}
    bad_dates = dict(y for y in data if y[0] in {x[0] for x in Counter([z[0] for z in data]).items() if x[1] == 1})
    data = {(x,y) for x,y in data if not (x in bad_dates.keys() or y in bad_dates.values())}
    data = {y for y in data if y[0] not in {x[0] for x in Counter(x[0] for x in data).items() if x[1] != 1}}
    res =  {y for y in data if y[1] not in {x[0] for x in Counter(x[1] for x in data).items() if x[1] != 1}}.pop()
    return ' '.join(res)

if __name__ == "__main__":
    s = requests.Session()
    s.post(HOST+"login", data={"username":USERNAME, "password":PASSWORD})
    text = s.get(HOST+"task").text
    while True:
        soup = BeautifulSoup(text, 'html.parser')
        data = soup.findAll('div',{'class':'task_button'})
        if not data:
            print(text)
            exit()
        print(soup.h1.text)
        answer = filter_data([x.text for x in data])
        text = s.post(HOST+"task", data={"answer":answer}).text