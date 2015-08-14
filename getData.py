import json
import urllib2

def prettyjson(arg):
    print json.dumps(arg, sort_keys=True, indent=4 , separators=(',', ': '))

"""

Static Data Handling

"""

handler =  urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?itemListData=gold,into&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
itemData = json.loads(handler.read())

#prettyjson(itemData['data'])

handler = urllib2.urlopen("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=62763b3a-0683-48f1-9efc-1fcad131299c")
champData = json.loads(handler.read())

#prettyjson(champData['data'])
#for key, pair in champData['data'].iteritems():
#    print pair['name']

"""

Data Storage Initialization

"""

champDict = {}
overallData = {}
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
            time.sleep(1000)
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
    for person in gameData['participants']:
        add = 'W' if person['participantId'] in winners else 'L'
        overallData[str(person['championId'])][add] += 1
        for i in range(7):
    #        print 'item'+str(i)
            if 'item'+str(i) in person['stats']:
                try:
                    champDict[str(person['championId'])][7][str(person['stats']['item'+str(i)])][add] += 1
                    #print 'itemadded'
                except KeyError:
                    continue
    #                print 'no item in this slot'

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
                ret['overallItemData'][item][str(i)]['W'] += champDict[champ][7][item].get('W',0)
                ret['overallItemData'][item][str(i)]['T'] += champDict[champ][7][item].get('T',0)
                ret['overallItemData'][item][str(i)]['L'] += champDict[champ][7][item].get('L',0)
                ret['overallItemData'][item][str(i)]['GP'] += champDict[champ][7][item].get('GP',0)
                ret['overallItemData'][item][str(i)]['D'] += champDict[champ][7][item].get('D',0)
                ret['overallItemData'][item][str(i)]['TE'] += champDict[champ][7][item].get('TE',0)
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
    ## Pick Rate of items
    ## Pick Rate of items given champion
    ## Pick Rate of items in certain slot
    ## Pick Rate of items in certain slot given champion
    return ret

analyze(1900729148)
ret = extractStatistics()
print ret['itemTimeChampion']['103']['3157']
