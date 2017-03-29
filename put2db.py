import redis
import re

r = redis.Redis()       # default local host

f = open('AMiner-Author.txt')
all_data = f.read()
all_data = all_data.split('#index ')
i = 0
try:
    for data in all_data:
        if i < 1712434:
            i += 1
            continue
        if i % 100 == 0:
            print i, ' of (domain)', len(all_data)
        i += 1
        if data == '':
            continue
        n = data.find('#n') + 3
        a = data.find('#a')
        name = data[n: a]
        ts = data.find('#t')
        interests = data[ts + 3: -1].split(';')
        for interest in interests:
            interest.replace('\n', '')
            r.lpush(interest, data)
except Exception:
    print i
f.close()

f = open('AMiner-Coauthor.txt')
corrs = f.read().split('\n')
i = 0
try:
    for corr in corrs:
        if i < 4258947:
            i += 1
            continue
        if i % 100 == 0:
            print i, ' of co-authors', len(corrs)
        i += 1
        corr = corr[1:]
        tmp = corr.split('\t')
        r.lpush(tmp[0], tmp[1] + ' ' + tmp[2])
        r.lpush(tmp[1], tmp[0] + ' ' + tmp[2])
except Exception:
    print i
f.close()

f = open('AMiner-Author.txt')
all_data = f.read()
all_data = all_data.split('#index ')
i = 0
try:
    for data in all_data:
        if i < 21431:
            i += 1
            continue
        if i % 100 == 0:
            print i, ' of (index)', len(all_data)
        i += 1
        if data == '':
            continue
        ind = re.search('(\d*)', data).group(1)
        r.set('#' + ind, data)
except Exception:
    print i
f.close()
