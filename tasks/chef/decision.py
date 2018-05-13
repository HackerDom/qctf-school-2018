from itertools import chain

with open('encoded.txt') as f: s = f.read()
l = [int(i) for i in s.split()]
i = 1
answ = []
for pair in zip(l[:16], l[16:]):
    answ += [chr(pair[0] - i), chr(pair[1] - i)]
    i += 1
print(''.join(answ))