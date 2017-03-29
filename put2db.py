import redis
import re

r = redis.Redis()       # default local host

f = open('AMiner-Author.txt')
all_data = f.read()
all_data = all_data.split('#index ')
i = 0
for data in all_data:
    if i % 100 == 0:
        print i, ' of ', len(all_data)
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
f.close()

f = open('AMiner-Coauthor.txt')
corrs = f.read().split('\n')
i = 0
for corr in corrs:
    if i % 100 == 0:
        print i, ' of ', len(corrs)
    i += 1
    corr = corr[1:]
    tmp = corr.split('\t')
    r.lpush(tmp[0], tmp[1] + ' ' + tmp[2])
    r.lpush(tmp[1], tmp[0] + ' ' + tmp[2])
f.close()

f = open('AMiner-Author.txt')
all_data = f.read()
all_data = all_data.split('#index ')
i = 0
for data in all_data:
    if i % 100 == 0:
        print i, ' of ', len(all_data)
    i += 1
    if data == '':
        continue
    ind = re.search('(\d*)', data).group(1)
    r.set('#' + ind, data)
f.close()
