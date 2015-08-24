from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from pages.models import JSON
import urllib2
import json
def init():
    try:
        global f
        a = f['overallChampionData']
    except Exception:
        print 'reopening'
        f1 = open('NA-5.14Analysis.json')
        global f
        f = json.loads(f1.read())
    # CHAMP PAGE STATISTICS

    # ITEM PAGE STATISTICS



    #a = JSON(value="root", done="F")
    #a.save()
    #recurse(f, a)
def recurse(lista, parent):
    if isinstance(lista, list):
        for i in range(len(lista)):
            #print i
            a = JSON(value=str(i), done="F")
            a.save()
            #print "saved"
            parent.entries.add(a)
            parent.save()
            #print "added to parent"
            recurse(lista[i], a)
    elif isinstance(lista, dict):
        #print lista.keys()
        for i in lista:
            #print i
            a = JSON(value=i, done="F")
            a.save()
            #print "saved dict"
            parent.entries.add(a)
            parent.save()
        #    print "added to parent dict"
            recurse(lista[i], a)
    else:
        print "TERMINAL ", lista
        a = JSON(value=str(lista), done="T")
        a.save()
        parent.entries.add(a)
        parent.save()

def table(request):
    init()
    show = {}
    wrlist = []

    ### VERY INEFFICIENT RIGHT NOW FIX SOON ###
    dir = True
    if dir:
        handler =  urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.14.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData = json.loads(handler.read())
    else:
        handler =  urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.11.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData = json.loads(handler.read())
    handler = urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
    champData = json.loads(handler.read())


    for champ in f['championItemOrderWR']:
        addlist = ['']
        for item in f['championItemOrderWR'][champ]:
            addlist.append(itemData['data'][item]['name'])
        wrlist.append(addlist)
        break
    for champ in f['championItemOrderWR']:
        addList = [champData['data'][champ]['name']]
        for item in f['championItemOrderWR'][champ]:
            addList.append(round(float(f['championItemOrderWR'][champ][item]['7']['W'])/
                (f['championItemOrderWR'][champ][item]['7']['W']+f['championItemOrderWR'][champ][item]['7']['L']), 3)
                if f['championItemOrderWR'][champ][item]['7']['W'] > 0
                else 0)
        wrlist.append(addList)
    show['wrlist'] = wrlist
    return render(request, 'pages/table.html', show)

def index(request):
    # try:
    #     root = JSON.objects.get(value="root")
    # except Exception:
    #     init()
    #     root = JSON.objects.get(value="root")
    init()
    show = {}

    # diana analysis
    # diana wr
    print f['overallChampionData']['131']
    show['wr'] = f['overallChampionData']['131']
    # diana pickrate
    print f['championPickRate']['131']
    show['pr'] = f['overallChampionData']['131']
    # diana picking abyssal wrs
    print f['championItemOrderWR']['131']['3001']
    # diana by highest wr item
    items = sorted(f['championItemOrderWR']['131'], key=lambda key:
            -float(f['championItemOrderWR']['131'][key]['7']['W'])/
            (f['championItemOrderWR']['131'][key]['7']['L']+
            f['championItemOrderWR']['131'][key]['7']['W'])
            if (f['championItemOrderWR']['131'][key]['7']['L']+
            f['championItemOrderWR']['131'][key]['7']['W']) > 50 else 0 )
    print items
    print len(items)
    show['item_list'] = []
    for i in range(5):
        print items[i]
        show['item_list'].append(items[i])
        print f['championItemOrderWR']['131'][items[i]]['7']['W']
        print f['championItemOrderWR']['131'][items[i]]['7']['L']
    return render(request, 'pages/index.html', show)
    """

    """
