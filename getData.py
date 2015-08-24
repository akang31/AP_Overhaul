import json
import urllib2

def prettyjson(arg):
    print json.dumps(arg, sort_keys=True, indent=4 , separators=(',', ': '))

"""

Static Data Handling

"""
itemData = {}
champData = {}


"""

Data Storage Initialization

"""

champDict = {}
overallData = {}
overallItemPickData = {}
# for key in itemData['data']:
#     overallItemPickData[key] = 0
# for key in champData['data']:
#     #print key
#     tempList = []
#     for i in range(8):
#         tempDict = {}
#         for key1 in itemData['data']:
#             tempDict[key1.rstrip().strip()] = {'W':0, 'L':0, 'T':0, 'GP':0, 'D':0, 'TE':0}
#         tempList.append(tempDict)
#     overallData[key.rstrip().strip()] = {'W':0, 'L':0}
#     champDict[key.rstrip().strip()] = tempList

def displayChampDict():
    for champ in champDict:
        for index in range(8):
            for item in champDict[champ][index]:
                for stat in champDict[champ][index][item]:
                    if champDict[champ][index][item][stat] > 0:
                        print str(champ) +" " + str(index) + " " + str(item) + " " + stat + " " + str(champDict[champ][index][item][stat])

"""

Method for single call handling

"""
import time
def analyze(matchId):
    while True:
        try:
            handler = urllib2.urlopen("https://na.api.pvp.net/api/lol/na/v2.2/match/"+str(matchId)+"?includeTimeline=true&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
            break
        except:
            print "requests overloaded, waiting"
            time.sleep(1)
    gameData = json.loads(handler.read())
    """
    Handle Post-Match Data:
        participants
            participantId
            championId
            teamId
            stats
                item[0-5]
        teams (array)
            teamId
            winner
    """

    winners = []
    people = {}
    winteam = -1
    global overallData
    global champDict
    for tem in gameData['teams']:
        if tem['winner']:
            winteam = tem['teamId']
    for person in gameData['participants']:
        if str(person['teamId']) == str(winteam):
            winners.append(person['participantId'])
        people[person['participantId']] = person['championId']
    itemsInGame = {}
    for person in gameData['participants']:
        add = 'W' if person['participantId'] in winners else 'L'
        overallData[str(person['championId'])][add] += 1
        for i in range(7):
    #        print 'item'+str(i)
            if 'item'+str(i) in person['stats']:
                try:
                    champDict[str(person['championId'])][7][str(person['stats']['item'+str(i)])][add] += 1
                    itemsInGame[person['stats']['item'+str(i)]] = 1
                    #print 'itemadded'
                except KeyError:
                    continue
    #                print 'no item in this slot'
    for key in itemsInGame:
        overallItemPickData[str(key)] += 1
    """
    Handle Timeline Data:
        timeline
            frameInterval
            frames (array)
                timestamp
                participantFrames
                [events] (array)
                    timestamp (ms)
                    eventType (ITEM_PURCHASED)
                    itemId
                    participantId
    """
    def isBoots(intid):
        boots = ['3117', '3009', '3158', '3020', '3006', '3047', '3111', '2045', '3092', '3401', '3069']
        return str(intid) in boots
    data = {}
    for num in people:
        data[num] = {'itemCount': 0, 'lastTime': 0, 'lastGold': 0, 'counting': 0, 'lastId': 0}
    for frame in gameData['timeline']['frames']:
        timestamp = frame['timestamp']
        peopleInfo = frame['participantFrames']
        if 'events' in frame:
            for event in frame['events']:
                if event['eventType'] == 'ITEM_PURCHASED':
                    add = 'W' if event['participantId'] in winners else 'L'
                    # GPM data between buys
                    if data[event['participantId']]['counting'] and not event['itemId'] == data[event['participantId']]['lastId']:
                        champDict[str(people[event['participantId']])][data[event['participantId']]['itemCount']-1][str(data[event['participantId']]['lastId'])]['TE'] += timestamp - data[event['participantId']]['lastTime']
                        champDict[str(people[event['participantId']])][data[event['participantId']]['itemCount']-1][str(data[event['participantId']]['lastId'])]['GP'] += peopleInfo[str(event['participantId'])]['totalGold'] - data[event['participantId']]['lastGold']
                        data[event['participantId']]['counting'] = 0
                    # Item Buy Updates
                    if (isBoots(event['itemId']) or int(itemData['data'][str(event['itemId'])]['gold']['total']) > 2000) and data[event['participantId']]['itemCount'] < 6 and not event['itemId'] == data[event['participantId']]['lastId']:
                        champDict[str(people[event['participantId']])][data[event['participantId']]['itemCount']][str(event['itemId'])][add] += 1
                        champDict[str(people[event['participantId']])][data[event['participantId']]['itemCount']][str(event['itemId'])]['T'] += event['timestamp']
    #                    print itemData['data'][str(event['itemId'])]['name']
    #                    print int(itemData['data'][str(event['itemId'])]['gold']['total'])
                        data[event['participantId']]['itemCount'] += 1
                        data[event['participantId']]['counting'] = 1
                        data[event['participantId']]['lastId'] = event['itemId']
                        data[event['participantId']]['lastTime'] = timestamp
                        data[event['participantId']]['lastGold'] = peopleInfo[str(event['participantId'])]['totalGold']
    # print frame
    # DO LAST FRAME SEPARATELY FOR UPDATING WHEN NEW ITEMS HAVE NOT YET BEEN RECORDED
    for i in range(1, 11):
        timestamp = frame['timestamp']
        peopleInfo = frame['participantFrames']
        add = 'W' if i in winners else 'L'
        # GPM data between buys
        if data[i]['counting']:
            #print str(timestamp) + " " + str(data[i]['lastTime'])
            #print str(i)+ " " + str(data[i]['lastId']) + " " + str(data[i]['itemCount'])
            champDict[str(people[i])][data[i]['itemCount']-1][str(data[i]['lastId'])]['TE'] += timestamp - data[i]['lastTime']
            champDict[str(people[i])][data[i]['itemCount']-1][str(data[i]['lastId'])]['GP'] += peopleInfo[str(i)]['totalGold'] - data[i]['lastGold']
            #print str(champDict[str(people[i])][data[i]['itemCount']-1][str(data[i]['lastId'])]['TE']) +  " "  + str(champDict[str(people[i])][data[i]['itemCount']-1][str(data[i]['lastId'])]['GP'] )
            data[i]['counting'] = 0
            #print str(people[i])
    #print str(champDict[str(people[2])][data[2]['itemCount']-1][str(data[2]['lastId'])]['TE']) +  " "  + str(champDict[str(people[2])][data[2]['itemCount']-1][str(data[2]['lastId'])]['GP'] )
    #print champDict['57'][4]['3800']
    #displayChampDict()
def extractStatistics():
    ret = {}
    # General W/L Data for items POST game (so index 7)
    ## Overall W/L for certain champions
    ret['overallChampionData'] = overallData
    ## Overall W/L/T/GP/D/TE for certain items
    ret['overallItemData'] = {}
    for item in itemData['data']:
        ret['overallItemData'][item] = {}
        for i in range(8):
            ret['overallItemData'][item][str(i)] = {'W':0, 'L':0, 'T':0, 'GP':0, 'D':0, 'TE':0}
    for champ in champDict:
        for item in itemData['data']:
            for i in range(8):
                ret['overallItemData'][item][str(i)]['W'] += champDict[champ][i][item].get('W',0)
                ret['overallItemData'][item][str(i)]['T'] += champDict[champ][i][item].get('T',0)
                ret['overallItemData'][item][str(i)]['L'] += champDict[champ][i][item].get('L',0)
                ret['overallItemData'][item][str(i)]['GP'] += champDict[champ][i][item].get('GP',0)
                ret['overallItemData'][item][str(i)]['D'] += champDict[champ][i][item].get('D',0)
                ret['overallItemData'][item][str(i)]['TE'] += champDict[champ][i][item].get('TE',0)
    ## W/L+GPM for certain champion given that they purchased a item at a certain timeline
    ret['championItemOrderWR'] = {}
    for champ in champDict:
        ret['championItemOrderWR'][champ] = {}
        for item in itemData['data']:
            ret['championItemOrderWR'][champ][item] = {}
            for i in range(8):
                ret['championItemOrderWR'][champ][item][str(i)] = champDict[champ][i][item]
    ## Average Time of Item Purchase Overall
    ret['itemTime'] = {}
    itemCount = {}
    for champ in champDict:
        for item in itemData['data']:
            for i in range(6):
                ret['itemTime'][item] = ret['itemTime'].get(item,0) + champDict[champ][i][item].get('T',0)
                itemCount[item] = itemCount.get(item, 0)  + champDict[champ][i][item].get('W',0)
                itemCount[item] = itemCount[item] + champDict[champ][i][item].get('L',0)
    for item in itemData['data']:
        if itemCount[item] > 0:
            ret['itemTime'][item] /= itemCount[item]
    ## Average Time of Item Purchase given champion
    ret['itemTimeChampion'] = {}
    itemCountChamp = {}
    for champ in champDict:
        ret['itemTimeChampion'][champ] = {}
        itemCountChamp[champ] = 0
        for item in itemData['data']:
            for i in range(6):
                ret['itemTimeChampion'][champ][item] =  ret['itemTimeChampion'][champ].get(item, 0) + champDict[champ][i][item].get('T',0)
                itemCountChamp[item] = itemCount.get(item,0)+ champDict[champ][i][item].get('W',0)
                itemCountChamp[item] += champDict[champ][i][item].get('L',0)
    ## Pick Rate of champions
    totalGames = 0
    for key in overallData:
        totalGames += overallData[key]['W']+overallData[key]['L']
    totalGames /= 10
    ret['championPickRate'] = {}
    for key in overallData:
        ret['championPickRate'][key] = (overallData[key]['W']+overallData[key]['L']) / float(totalGames)
    ## Pick Rate of items
    ret['itemPickRate'] = {}
    for key in overallItemPickData:
        ret['itemPickRate'][key] = overallItemPickData[key] / float(totalGames)
    ## Average number of item bought per game
    ret['avgItemPerGame'] = {}
    for item in itemData['data']:
        ret['avgItemPerGame'][item] = 0
    for champ in champDict:
        for item in itemData['data']:
            ret['avgItemPerGame'][item] += champDict[champ][7][item]['W'] + champDict[champ][7][item]['L']
    for item in itemData['data']:
        if ret['avgItemPerGame'][item] > 0:
            ret['avgItemPerGame'][item] /= float(overallItemPickData[item])
    ## Pick Rate of items given champion
    ret['itemPickRateChampion'] = {}
    for champ in champDict:
        ret['itemPickRateChampion'][champ] = {}
        for item in itemData['data']:
            if champDict[champ][7][item]['W']+champDict[champ][7][item]['L'] > 0:
                ret['itemPickRateChampion'][champ][item] = (champDict[champ][7][item]['W']+champDict[champ][7][item]['L'])/float(overallData[champ]['W']+overallData[champ]['L'])

    ## Pick Rate of items in certain slot

    ## Pick Rate of items in certain slot given champion

    return ret

def initialize(dir):
    global itemData
    global champData
    if dir:
        handler =  urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.14.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData = json.loads(handler.read())
    else:
        handler =  urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?version=5.11.1&itemListData=gold&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
        itemData = json.loads(handler.read())


    #prettyjson(itemData['data'])

    handler = urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
    champData = json.loads(handler.read())

    #prettyjson(champData['data'])
    #for key, pair in champData['data'].iteritems():
    #    print pair['name']
    global champDict
    global overallData
    global overallItemPickData
    champDict = {}
    overallData = {}
    overallItemPickData = {}
    for key in itemData['data']:
        overallItemPickData[key] = 0
    for key in champData['data']:
        #print key
        tempList = []
        for i in range(8):
            tempDict = {}
            for key1 in itemData['data']:
                tempDict[key1.rstrip().strip()] = {'W':0, 'L':0, 'T':0, 'GP':0, 'D':0, 'TE':0}
            tempList.append(tempDict)
        overallData[key.rstrip().strip()] = {'W':0, 'L':0}
        champDict[key.rstrip().strip()] = tempList


def doAll():
    f1 = open('NA-5.11.json')
    games511 = json.loads(f1.read())
    initialize(False)
    for i in games511:
        print "511 ",i
        analyze(i)
    json511 = extractStatistics()

    f3 = open('NA-5.11Analysis.json', 'w')
    f3.write(json.dumps(json511))

    f2 = open('NA-5.14.json')
    games514 = json.loads(f2.read())
    initialize(True)
    for i in games514:
        print "514 ",i
        analyze(i)
    json514 = extractStatistics()

    f4 = open('NA-5.14Analysis.json', 'w')
    f4.write(json.dumps(json514))

# initialize()
# analyze(1900729148)
# ret = extractStatistics()
# print ret['itemTimeChampion']['103']['3157']

doAll()
