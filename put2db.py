import redis
import re

r = redis.Redis()       # default local host

# f = open('Aminer-Author.txt')
# all_data = f.read()
# all_data = all_data.split('#index ')
# for data in all_data:
#     if data == '':
#         continue
#     n = data.find('#n') + 3
#     a = data.find('#a')
#     name = data[n: a]
#     ts = data.find('#t')
#     interests = data[ts + 3: -1].split(';')
#     for interest in interests:
#         interest.replace('\n', '')
#         r.lpush(interest, data)

f = open('Aminer-Coauthor.txt')
corrs = f.read().split('\n')
i = 0
for corr in corrs:
    print i, ' of ', len(corrs)
    i += 1
    corr = corr[1:]
    tmp = corr.split('\t')
    r.lpush(tmp[0], tmp[1] + ' ' + tmp[2])
    r.lpush(tmp[1], tmp[0] + ' ' + tmp[2])

# f = open('Aminer-Author.txt')
# all_data = f.read()
# all_data = all_data.split('#index ')
# for data in all_data:
#     print 'fuck'
#     if data == '':
#         continue
#     ind = re.search('(\d*)', data).group(1)
#     r.set('#' + ind, data)

