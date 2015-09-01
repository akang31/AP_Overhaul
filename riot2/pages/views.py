from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from pages.models import JSON
import urllib2
import json
def init():
    """
    Initialization for static data and calculated data. Stored globally by instance.
    """
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
        handler514 =  open('item514.txt')
        itemData514 = json.loads(handler514.read())
        handler511 =  open('item511.txt')
        itemData511 = json.loads(handler511.read())
        handler = open('champ.txt')
        champData = json.loads(handler.read())

import time
def champPage(request, champID):
    """
    Generates champion page based in champID.
    """
    init()
    show = {}

    show['champName'] = champData['data'][str(champID)]['name']
    show['champImage'] = '"/static/img/champs/'+str(idToChamp[str(champID)])+'"'

    # Calculate most popular items in order of which they are built (ie. most popular items to buy first, second etc)
    itemSlotRank514 = []
    for i in range(6):
        add1 = []
        for j in itemData514['data']:
            add1.append((str(j), f['championItemOrderWR'][str(champID)][str(j)][str(i)]['W']+f['championItemOrderWR'][str(champID)][str(j)][str(i)]['L']))# getWR(f['championItemOrderWR'][str(champID)][str(j)][str(i)])))
        add1 = sorted(add1, key=lambda key: -key[1])
        add = {'item1': add1[0][0], 'item2': add1[1][0], 'item3':add1[2][0], 'notlast': (not i == 5)}
        itemSlotRank514.append(add)
    show['item_list'] = itemSlotRank514

    # Highest win rate items from 511
    itemList_511 = []
    items = sorted(g['championItemOrderWR'][str(champID)], key=lambda key:
            -getWR(g['championItemOrderWR'][str(champID)][key]['7']))
    for i in range(1,10):
        add = {}
        add['order'] = '"order'+str(i)+'"'
        add['img'] = '"/static/img/511/'+str(items[i])+'.png"'
        add['name'] = itemData511['data'][str(items[i])]['name']
        add['wr'] = str(getWR(g['championItemOrderWR'][str(champID)][str(items[i])]['7']))+'%'
        add['pr'] = str(round(g['itemPickRateChampion'][str(champID)][str(items[i])], 4)*100)+'%'
        itemList_511.append(add)
    show['item_list511'] = itemList_511

    # Highest win rate items from 514
    itemList_514 = []
    items = sorted(f['championItemOrderWR'][str(champID)], key=lambda key:
            -getWR(f['championItemOrderWR'][str(champID)][key]['7']))
    for i in range(1,10):
        add = {}
        add['order'] = '"order'+str(i)+'"'
        add['img'] = '"/static/img/514/'+str(items[i])+'.png"'
        add['name'] = itemData514['data'][str(items[i])]['name']
        add['wr'] = str(getWR(f['championItemOrderWR'][str(champID)][str(items[i])]['7']))+'%'
        add['pr'] = str(round(f['itemPickRateChampion'][str(champID)][str(items[i])], 4)*100)+'%'
        itemList_514.append(add)
    show['item_list514'] = itemList_514

    # Pickrate Data
    show['pr511'] = round(g['championPickRate'][str(champID)],4)*100
    show['pr514'] = round(f['championPickRate'][str(champID)],4)*100
    show['PRdiff'] = show['pr514']-show['pr511']
    show['prn'] = show['PRdiff'] < 0
    show['pr511'] = str(show['pr511'])+'%'
    show['pr514'] = str(show['pr514'])+'%'
    show['PRdiff'] = str(show['PRdiff'])+'%'

    #Winrate Data
    show['wr511'] = round(getWR(g['overallChampionData'][str(champID)]), 3)
    show['wr514'] = round(getWR(f['overallChampionData'][str(champID)]), 3)
    show['WRdiff'] = show['wr514']-show['wr511']
    show['wrn'] = show['WRdiff'] < 0
    show['wr511'] = str(show['wr511'])+'%'
    show['wr514'] = str(show['wr514'])+'%'
    show['WRdiff'] = str(show['WRdiff'])+'%'
    return render(request, 'pages/champPage.html', show)

def about(request):
    """
    About page. No further templating necessary
    """
    init()
    return render(request, 'pages/about.html', {})

def table(request):
    return ""

def itemPage(request, itemID):
    """
    ItemPage generation based on itemID
    """
    init()
    show = {}
    # Basic item stats
    show['itemName'] = itemData511['data'][str(itemID)]['name']
    show['icon'] = '/static/img/511/'+str(itemID)+".png"
    show['itemRawStats511'] = itemData511['data'][str(itemID)]['description']
    show['itemCost511'] = itemData511['data'][str(itemID)]['gold']['total']
    show['itemRawStats514'] = itemData514['data'][str(itemID)]['description']
    show['itemCost514'] = itemData514['data'][str(itemID)]['gold']['total']

    itemlist = []

    def indexOfIn(cid , array):
        for i in range(len(array)):
            if cid == array[i][0]:
                print array[i][1]
                return i
        return -1

    # Stats for item ranking (global)
    for item in f['overallItemData']:
        itemlist.append((item, getWR(f['overallItemData'][item]['7'])))
    itemlist = sorted(itemlist, key = lambda a: -a[1] if str(a[0]) in g['overallItemData'] else 1)
    itemlist1 = []
    for item in g['overallItemData']:
        itemlist1.append((item, getWR(g['overallItemData'][item]['7'])))
    itemlist1 = sorted(itemlist1, key = lambda a: -a[1] if str(a[0]) in f['overallItemData'] else 1)
    show['rank511'] = indexOfIn(str(itemID), itemlist1)+1
    show['rank514'] = indexOfIn(str(itemID), itemlist)+1
    show['rankdiff'] = -show['rank514']+show['rank511']
    show['rn'] = show['rankdiff'] < 0

    # Calculate and display GPM stats from 5.11 to 5.14 for each item
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
    show['GPM511'] = round(float(gtot1*60000)/ttot1, 2) if ttot1 > 0 else 0
    show['GPM514'] = round(float(gtot2*60000)/ttot2, 2) if ttot2 > 0 else 0
    show['GPMdiff'] = show['GPM514']-show['GPM511']
    show['GPMn'] = show['GPMdiff'] < 0

    # Winrate changes from 5.11 to 5.14
    show['WR511'] = getWR(g['overallItemData'][str(itemID)]['7'])
    show['WR514'] = getWR(f['overallItemData'][str(itemID)]['7'])
    show['WRdiff'] = -show['WR511']+show['WR514']
    show['WRn'] = show['WRdiff'] < 0
    show['WRdiff'] = str(show['WRdiff'])+'%'
    show['WR511'] = str(show['WR511'])+'%'
    show['WR514'] = str(show['WR514'])+'%'

    # Pickrate changes from 5.11 to 5.14
    show['pickRate511'] = round(g['itemPickRate'][str(itemID)], 4)*100
    show['pickRate514'] = round(f['itemPickRate'][str(itemID)], 4)*100
    show['pickRateDiff'] = show['pickRate514'] - show['pickRate511']
    show['PRn'] = show['pickRateDiff'] < 0
    show['pickRate511'] = str(show['pickRate511'])+'%'
    show['pickRate514'] = str(show['pickRate514'])+'%'
    show['pickRateDiff'] = str(show['pickRateDiff'])+'%'

    # Time of completion calculations
    show['completion511'] = round(float(g['itemTime'][str(itemID)])/60000, 2)
    show['completion514'] = round(float(f['itemTime'][str(itemID)])/60000, 2)
    show['completionDiff'] = show['completion514']-show['completion511']
    show['cn'] = show['completionDiff'] < 0

    # Calculate champions with highest WR following patch and pickrate following patch along with rank change

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
    return render(request, 'pages/itemPage.html', show)


def getWR(data):
    """
    Give WR based on a list containing Wins and Losses. Only give a winrate when there are more than 30 games of data, round to 4 and give as a percent.
    """
    return round(float(data['W'])/(data['W']+data['L']) if data['W']+data['L'] > 30 else 0, 4)*100

def index(request):
    """
    Index page.
    """
    init()
    show = {}
    itemlist = []

    def indexOfIn(cid , array):
        for i in range(len(array)):
            if cid == array[i][0]:
                print array[i][1]
                return i
        return -1
    # Create ranked list data, including winrates, pickrates, and rankings along with the changes.
    for item in f['overallItemData']:
        if f['itemPickRate'][item] > 0:
            itemlist.append((item, getWR(f['overallItemData'][item]['7'])))
    itemlist = sorted(itemlist, key = lambda a: -a[1] if str(a[0]) in g['overallItemData'] else 1)
    itemlist1 = []
    for item in g['overallItemData']:
        if g['itemPickRate'][item] > 0:
            itemlist1.append((item, getWR(g['overallItemData'][item]['7'])))
    itemlist1 = sorted(itemlist1, key = lambda a: -a[1] if str(a[0]) in f['overallItemData'] else 1)
    item_list = []
    for i in range(len(itemlist)):
        add = {}
        add['rank'] = str(i+1)
        print i
        if not str(itemlist[i][0]) in g['overallItemData']:
            continue
        add['name'] = itemData511['data'][str(itemlist[i][0])]['name']
        add['id'] = str(itemlist[i][0])
        add['wr511'] = str(getWR(g['overallItemData'][str(itemlist[i][0])]['7'])) + '%'
        add['wr514'] = str(getWR(f['overallItemData'][str(itemlist[i][0])]['7'])) + '%'
        add['pr511'] = str(round(g['itemPickRate'][str(itemlist[i][0])],4)*100) + '%'
        add['pr514'] = str(round(f['itemPickRate'][str(itemlist[i][0])],4)*100) + '%'
        add['rankChange'] = -  i + indexOfIn(itemlist[i][0], itemlist1)
        add['rn'] = add['rankChange'] < 0
        item_list.append(add)
    show['item_list'] = item_list
    return render(request, 'pages/index.html', show)
