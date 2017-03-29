from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import redis
import os
import re
import requests


class prof:
    def __init__(self, data):
        tmp = re.search(r'\s*(\d*)\n#n\s*(.*)\n#a(.*)\n#pc.*\n#cn.*\n#hi\s*(\d*).*', data, re.DOTALL | re.M)
        self.id = tmp.group(1)
        self.name = tmp.group(2)
        self.affiliations = tmp.group(3)
        self.h_index = int(tmp.group(4))


client_id = '6580b23da11cade96de4'
client_secret = '8241080482ce19be25c1a66ed142201f677d80c6'
token_url = 'https://github.com/login/oauth/access_token'
api_url = 'https://api.github.com/user?access_token='


def get_h(p):
    return -p.h_index

def get_times(pair):
    return -int(pair[1])


# Create your views here.
def login(request):
    p = os.path.abspath('.')
    # print(p)
    oauth_dict = {'cli_id': client_id}
    return render(request, 'login.html', oauth_dict)


def index(request):
    code = request.GET.get('code')
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'code': code
    }
    headers = {'Accept': 'application/json'}    # to parse the response as json
    res = requests.post(token_url, data=data, headers=headers)
    res_jsn = res.json()
    token = res_jsn['access_token']
    ue_res = requests.get(api_url + token)
    ue_jsn = ue_res.json()

    return render(request, 'index.html', {'user': ue_jsn['login'], 'email': ue_jsn['email']})


def search(request):
    print 'we got a search', request.GET.get('domains')
    r = redis.Redis()
    domains = request.GET['domains']
    res = r.lrange(domains, 0, -1)
    lis = []
    for one_prof in res:
        lis.append(prof(one_prof))
    lis.sort(key=get_h)
    res = []
    for item in lis:
        res.append({'name': item.name, 'h': item.h_index, 'id': item.id})
    print res
    return JsonResponse({'experts': res})


def co_authors(request):
    prof_id = request.GET.get('id')
    print prof_id
    r = redis.Redis()
    co_aus = r.lrange(prof_id, 0, -1)
    print co_aus
    res = []
    for coau in co_aus:
        index_times = coau.split(' ')
        res.append(index_times)
    res.sort(key=get_times)
    coau_res = []
    for ind in res:
        all_info = r.get('#' + ind[0])
        name = re.search(r'#n\s*(.*)\s', all_info)
        coau_res.append({'name': name.group(1), 't': ind[1]})
    print coau_res
    return render(request, 'coauthors.html', {'lis': coau_res})
