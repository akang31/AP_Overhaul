from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from pages.models import JSON
import urllib2
import json
def init():
    working = 0
    try:
        global f
        a = f['championPickRate']
        working = 1
    except Exception:
        print 'reopening'
        f1 = open('NA-5.14Analysis.json')
        global f
        f = json.loads(f1.read())
    try:
        global g
        a = g['championPickRate']
        working = 1
    except Exception:
        print 'reopening'
        f2 = open('NA-5.11Analysis.json')
        global g
        g = json.loads(f2.read())
    if working == 0:
        f3 = open('idToChamp.txt')
        global idToChamp
        idToChamp = json.loads(f3.read())
        global itemData511
        global itemData514
        global champData
        handler514 =  open('item514.txt')#urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.14.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData514 = json.loads(handler514.read())
        handler511 =  open('item511.txt')#urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.11.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData511 = json.loads(handler511.read())
        handler = open('champ.txt')#urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        champData = json.loads(handler.read())

def table(request):
    init()
    show = {}
    wrlist = []

    ### VERY INEFFICIENT RIGHT NOW FIX SOON ###
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
import time
def champPage(request, champID):

    init()
    t0 = time.time()
    show = {}
    show['champName'] = champData['data'][str(champID)]['name']
    show['champImage'] = '"/static/img/champs/'+str(idToChamp[str(champID)])+'"'
    itemList_511 = []
    items = sorted(g['championItemOrderWR'][str(champID)], key=lambda key:
            -float(g['championItemOrderWR'][str(champID)][key]['7']['W'])/
            (g['championItemOrderWR'][str(champID)][key]['7']['L']+
            g['championItemOrderWR'][str(champID)][key]['7']['W'])
            if (g['championItemOrderWR'][str(champID)][key]['7']['L']+
            g['championItemOrderWR'][str(champID)][key]['7']['W']) > 50 else 0 )
    for i in range(1,10):
        add = {}
        add['order'] = '"order'+str(i)+'"'
        add['img'] = '"/static/img/511/'+str(items[i])+'.png"'
        add['name'] = itemData511['data'][str(items[i])]['name']
        itemList_511.append(add)
    show['item_list511'] = itemList_511
    itemList_514 = []
    items = sorted(f['championItemOrderWR'][str(champID)], key=lambda key:
            -float(f['championItemOrderWR'][str(champID)][key]['7']['W'])/
            (f['championItemOrderWR'][str(champID)][key]['7']['L']+
            f['championItemOrderWR'][str(champID)][key]['7']['W'])
            if (f['championItemOrderWR'][str(champID)][key]['7']['L']+
            f['championItemOrderWR'][str(champID)][key]['7']['W']) > 50 else 0 )
    for i in range(1,10):
        add = {}
        add['order'] = '"order'+str(i)+'"'
        add['img'] = '"/static/img/514/'+str(items[i])+'.png"'
        add['name'] = itemData514['data'][str(items[i])]['name']
        itemList_514.append(add)
    show['item_list514'] = itemList_514
    t1 = time.time()

    total = t1-t0
    print str(total) + " TIMING DATA"
    return render(request, 'pages/champPage.html', show)
import re
def itemPage(request, itemID):
    init()
    t0 = time.time()
    show = {}
    # wr 511
    show['itemName'] = itemData511['data'][str(itemID)]['name']
    show['icon'] = '/static/img/511/'+str(itemID)+".png"
    show['itemRawStats511'] = re.findall('<stats>(.*?)<\\\/stats\>', itemData511['data'][str(itemID)]['description'], re.DOTALL) if 'stats' in itemData511['data'][str(itemID)]['description'] else ''
    show['itemPassiveStats511'] = re.findall('<unique>(.*?)<\\\/unique\>', itemData511['data'][str(itemID)]['description'], re.DOTALL) + re.findall('<\\\/unique\>(.*?)', itemData511['data'][str(itemID)]['description'], re.DOTALL) if 'unique' in itemData511['data'][str(itemID)]['description'] else ''
    show['itemActiveStats511'] = "dinosaur"
    show['itemCost511'] = itemData511['data'][str(itemID)]['gold']['total']
    show['itemRawStats514'] = re.findall('<stats>(.*?)<\\\/stats\>', itemData514['data'][str(itemID)]['description'], re.DOTALL) if 'stats' in itemData514['data'][str(itemID)]['description'] else ''
    show['itemPassiveStats514'] = re.findall('<unique>(.*?)<\\\/unique\>', itemData514['data'][str(itemID)]['description'], re.DOTALL) + re.findall('<\\\/unique\>(.*?)', itemData514['data'][str(itemID)]['description'], re.DOTALL) if 'unique' in itemData514['data'][str(itemID)]['description'] else ''
    show['itemActiveStats514'] = "dinosaur"
    show['itemCost514'] = itemData514['data'][str(itemID)]['gold']['total']

    show['GPM511'] = 1
    show['GPM514'] = 1
    show['GPMdiff'] = 1
    show['WR511'] = getWR(g['overallItemData'][str(itemID)]['7'])
    show['WR514'] = getWR(f['overallItemData'][str(itemID)]['7'])
    show['WRdiff'] = -show['WR511']+show['WR514']
    show['iscore511'] = 1
    show['iscore514'] = 1
    show['iscorediff'] = 1
    show['pickRate511'] = g['itemPickRate'][str(itemID)]
    show['pickRate514'] = f['itemPickRate'][str(itemID)]
    show['pickRateDiff'] = show['pickRate514'] - show['pickRate511']
    show['completion511'] = g['itemTime'][str(itemID)]
    show['completion514'] = f['itemTime'][str(itemID)]
    show['completionDiff'] = show['completion514']-show['completion511']
    show['rank511'] = 1
    show['rank514'] = 1
    show['rankdiff'] = 1
    ranks511 = []
    for i in range(5):
        add = {}
        add['rank'] = i+1
        add['box'] = '\'{"icon":"/static/img/champs/wukong.png", "name":"Wukong", "delta":"2"}\''
        ranks511.append(add)
    show['ranked_511'] = ranks511
    ranks514 = []
    for i in range(5):
        add = {}
        add['rank'] = i+1
        add['box'] = '\'{"icon":"/static/img/champs/wukong.png", "name":"Wukong", "delta":"2"}\''
        ranks514.append(add)
    show['ranked_514'] = ranks514
    t1 = time.time()

    total = t1-t0
    print str(total) + " TIMING DATA"
    return render(request, 'pages/itemPage.html', show)


def getWR(data):
    return float(data['W'])/(data['W']+data['L']) if data['W'] > 0 else 0
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
