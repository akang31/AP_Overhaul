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
            g['championItemOrderWR'][str(champID)][key]['7']['W']) > 30 else 0 )
    for i in range(1,10):
        add = {}
        add['order'] = '"order'+str(i)+'"'
        add['img'] = '"/static/img/511/'+str(items[i])+'.png"'
        add['name'] = itemData511['data'][str(items[i])]['name']
        add['wr'] = round(getWR(g['championItemOrderWR'][str(champID)][str(items[i])]['7']), 3)
        add['pr'] = round(g['itemPickRateChampion'][str(champID)][str(items[i])], 3)
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
        add['wr'] = round(getWR(f['championItemOrderWR'][str(champID)][str(items[i])]['7']),3)
        add['pr'] = round(f['itemPickRateChampion'][str(champID)][str(items[i])], 3)
        itemList_514.append(add)
    show['item_list514'] = itemList_514
    t1 = time.time()
    show['pr511'] = g['championPickRate'][str(champID)]
    show['pr514'] = f['championPickRate'][str(champID)]
    show['PRdiff'] = show['pr514']-show['pr511']
    show['prn'] = show['PRdiff'] < 0
    show['wr511'] = round(getWR(g['overallChampionData'][str(champID)]), 3)
    show['wr514'] = round(getWR(f['overallChampionData'][str(champID)]), 3)
    show['WRdiff'] = show['wr514']-show['wr511']
    show['wrn'] = show['WRdiff'] < 0
    total = t1-t0
    print str(total) + " TIMING DATA"
    return render(request, 'pages/champPage.html', show)

def about(request):
    init()
    return render(request, 'pages/about.html', {})

import re
def itemPage(request, itemID):
    init()
    t0 = time.time()
    show = {}
    # wr 511
    show['itemName'] = itemData511['data'][str(itemID)]['name']
    show['icon'] = '/static/img/511/'+str(itemID)+".png"
    print itemData511['data'][str(itemID)]['description']
    show['itemRawStats511'] = re.findall('<stats>(.*?)<\\/stats>', itemData511['data'][str(itemID)]['description'], re.DOTALL)[0] if 'stats' in itemData511['data'][str(itemID)]['description'] else ''
    show['itemPassiveStats511'] = re.findall('<unique>(.*?)<\\/unique>', itemData511['data'][str(itemID)]['description'], re.DOTALL) + re.findall('<\\\/unique\>(.*?)', itemData511['data'][str(itemID)]['description'], re.DOTALL) if 'unique' in itemData511['data'][str(itemID)]['description'] else ''
    show['itemActiveStats511'] = "dinosaur"
    show['itemCost511'] = itemData511['data'][str(itemID)]['gold']['total']
    show['itemRawStats514'] = re.findall('<stats>(.*?)<\\/stats>', itemData514['data'][str(itemID)]['description'], re.DOTALL)[0] if 'stats' in itemData514['data'][str(itemID)]['description'] else ''
    show['itemPassiveStats514'] = re.findall('<unique>(.*?)<\\/unique>', itemData514['data'][str(itemID)]['description'], re.DOTALL) + re.findall('<\\\/unique\>(.*?)', itemData514['data'][str(itemID)]['description'], re.DOTALL) if 'unique' in itemData514['data'][str(itemID)]['description'] else ''
    show['itemActiveStats514'] = itemData514['data'][str(itemID)]['description']
    show['itemCost514'] = itemData514['data'][str(itemID)]['gold']['total']

    gtot1 = 0
    ttot1 = 0
    gtot2 = 0
    ttot2 = 0
    for champ in champData['data']:
        for i in range(6):
            gtot1 += g['championItemOrderWR'][champ][str(itemID)][str(i)]['GP']
            ttot1 += g['championItemOrderWR'][champ][str(itemID)][str(i)]['TE']
            gtot2 += f['championItemOrderWR'][champ][str(itemID)][str(i)]['GP']
            ttot2 += f['championItemOrderWR'][champ][str(itemID)][str(i)]['TE']
    show['GPM511'] = round(float(gtot1*60000)/ttot1, 3) if ttot1 > 0 else 0
    show['GPM514'] = round(float(gtot2*60000)/ttot2, 3) if ttot2 > 0 else 0
    show['GPMdiff'] = show['GPM514']-show['GPM511']

    show['GPMn'] = show['GPMdiff'] < 0

    show['WR511'] = round(getWR(g['overallItemData'][str(itemID)]['7']), 3)
    show['WR514'] = round(getWR(f['overallItemData'][str(itemID)]['7']), 3)
    show['WRdiff'] = -show['WR511']+show['WR514']

    show['WRn'] = show['WRdiff'] < 0

    show['iscore511'] = 1
    show['iscore514'] = 1
    show['iscorediff'] = 1
    show['pickRate511'] = g['itemPickRate'][str(itemID)]
    show['pickRate514'] = f['itemPickRate'][str(itemID)]
    show['pickRateDiff'] = show['pickRate514'] - show['pickRate511']

    show['PRn'] = show['pickRateDiff'] < 0

    show['completion511'] = round(float(g['itemTime'][str(itemID)])/60000, 3)
    show['completion514'] = round(float(f['itemTime'][str(itemID)])/60000, 3)
    show['completionDiff'] = show['completion514']-show['completion511']

    show['cn'] = show['completionDiff'] < 0

    show['rank511'] = 1
    show['rank514'] = 1
    show['rankdiff'] = 1

    show['rn'] = show['rankdiff'] < 0

    def indexOfIn(cid , array):
        for i in range(len(array)):
            if cid == array[i][0]:
                print array[i][1]
                return i
        return -1
    flistwr = []
    for champ in f['championItemOrderWR']:
        flistwr.append((champ, getWR(g['championItemOrderWR'][champ][str(itemID)]['7'])))
    flistwr = sorted(flistwr, key = lambda champ: -float(champ[1]))

    glistwr = []
    for champ in g['championItemOrderWR']:
        glistwr.append((champ, getWR(f['championItemOrderWR'][champ][str(itemID)]['7'])))
    glistwr = sorted(glistwr, key = lambda champ: -float(champ[1]))

    flistpr = []
    for champ in f['itemPickRateChampion']:
        try:
            flistpr.append((champ, g['itemPickRateChampion'][champ][str(itemID)]))
        except Exception:
            flistpr.append((champ, '0'))
    flistpr = sorted(flistpr, key = lambda champ: -float(champ[1]))

    glistpr = []
    for champ in g['itemPickRateChampion']:
        try:
            glistpr.append((champ, f['itemPickRateChampion'][champ][str(itemID)]))
        except Exception:
            glistpr.append((champ, '0'))
    glistpr = sorted(glistpr, key = lambda champ: -float(champ[1]))

    ranks511 = []
    for i in range(5):
        add = {}
        add['rank'] = i+1
        add['box'] = '\'{"icon":"/static/img/champs/' + idToChamp[str(glistwr[i][0])]+'", "name":"' + champData['data'][str(glistwr[i][0])]['name'].replace('\'', "")+'", "delta": "' + str(- i + indexOfIn(glistwr[i][0], flistwr)) + '"}\''
        print glistwr[i]
        ranks511.append(add)
    show['ranked_511'] = ranks511
    ranks514 = []
    for i in range(5):
        add = {}
        add['rank'] = i+1
        add['box'] = '\'{"icon":"/static/img/champs/' + idToChamp[str(glistpr[i][0])]+'", "name":"' + champData['data'][str(glistpr[i][0])]['name'].replace('\'', "")+'", "delta": "' + str(- i + indexOfIn(glistpr[i][0], flistpr)) + '"}\''
        ranks514.append(add)
    show['ranked_514'] = ranks514
    t1 = time.time()

    total = t1-t0
    print str(total) + " TIMING DATA"
    return render(request, 'pages/itemPage.html', show)


def getWR(data):
    return float(data['W'])/(data['W']+data['L']) if data['W']+data['L'] > 30 else 0
def index(request):
    init()
    show = {}
    itemlist = []
    for item in f['overallItemData']:
        itemlist.append((item, getWR(f['overallItemData'][item]['7'])))
    itemlist = sorted(itemlist, key = lambda a: -a[1] if str(a[0]) in g['overallItemData'] else 0)
    item_list = []
    for i in range(15):
        add = {}
        add['rank'] = str(i+1)
        add['name'] = itemData511['data'][str(itemlist[i][0])]['name']
        add['id'] = str(itemlist[i][0])
        add['wr511'] = getWR(g['overallItemData'][str(itemlist[i][0])]['7'])
        try:
            add['wr514'] = getWR(f['overallItemData'][str(itemlist[i][0])]['7'])
        except Exception:
            add['wr514'] = 'N/A'
        add['pr511'] = g['itemPickRate'][str(itemlist[i][0])]
        try:
            add['pr514'] = f['itemPickRate'][str(itemlist[i][0])]
        except Exception:
            add['pr514'] = 'N/A'
        item_list.append(add)
    show['item_list'] = item_list
    return render(request, 'pages/index.html', show)
    """

    """
