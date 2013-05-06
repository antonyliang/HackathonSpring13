"""
<A basic resource allocation program written for a Morgan Stanley Hackathon>
    Copyright (C) 2013  Team Midas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import socket
import math
import operator
import os
import sys

#f = open(os.devnull, "w")
#sys.stdout = f

#Globals
Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

goingDownJava = {}
goingDownData = {}

goingUpWeb = {}
goingUpJava = {}
goingUpData = {}

Demand = {}
DistW = {}
DistJ = {}
DistD ={}
ConfigW = {}
ConfigJ = {}
ConfigD = {}
secondProjArr = {}
thirdProjArr = {}

foo = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creates a connection to the game server and starts the game
def init():
    initArrays()
    global s
    s.connect(("hackathon.hopto.org", 63335))
    s.send("INIT Midas")
    data = s.recv(1024)
    print data
    s.send("RECD")
    data = s.recv(1024)
    print data
    parseCost(data)
    s.send("START")
    data = s.recv(1024)
    return data

#initalizes the server queue with zeroes
def initArrays():
    global goingDownJava
    global goingDownData

    global goingUpWeb
    global goingUpJava
    global goingUpData

    goingDownJava["NA"] = []
    goingDownJava["EU"] = []
    goingDownJava["AP"] = []
    for i in goingDownJava:
        goingDownJava[i].append(0)
        goingDownJava[i].append(0)

    goingUpWeb["NA"] = []
    goingUpWeb["EU"] = []
    goingUpWeb["AP"] = []
    goingDownData["NA"] = []
    goingDownData["EU"] = []
    goingDownData["AP"] = []

    for i in goingUpWeb:
        for j in range(0,3):
            goingUpWeb[i].append(0)
            goingDownData[i].append(0)

    goingUpJava["NA"] = []
    goingUpJava["EU"] = []
    goingUpJava["AP"] = []

    for i in goingUpJava:
        for j in range(0,5):
            goingUpJava[i].append(0)

    goingUpData["NA"] = []
    goingUpData["EU"] = []
    goingUpData["AP"] = []

    for i in goingUpData:
        for j in xrange(0,9):
            goingUpData[i].append(0)

def printArrays():
    global goingDownJava
    global goingDownData

    global goingUpWeb
    global goingUpJava
    global goingUpData

    for i in ["NA", "EU", "AP"]:
        print "COMING DOWN IN " + i + ": "
        print "JAVA"
        print goingDownJava[i]
        print "DATA"
        print goingDownData[i]

        print "COMING UP IN " + i + ": "
        print "WEB"
        print goingUpWeb[i]
        print "JAVA"
        print goingUpJava[i]
        print "DATA"
        print goingUpData[i]


#moves the servers in queue down in one turn
#those coming online next turn get considered as basically online and vice versa
def passArrayTime():
    global goingDownJava
    global goingDownData

    global goingUpWeb
    global goingUpJava
    global goingUpData

    global ConfigW
    global ConfigJ
    global ConfigD

    for i in ["NA", "EU", "AP"]:
        if (goingDownJava[i][0] > 0 ):
#            ConfigJ[i] = ConfigJ[i] - goingDownJava[i][0]
            goingDownJava[i][0] = 0

        for j in range(1,len(goingDownJava[i])):
            goingDownJava[i][j-1] = goingDownJava[i][j]
#            if (i == 1 or i == 2):
#                ConfigJ[i] = ConfigJ[i] - goingDownJava[i][j]
            goingDownJava[i][j] = 0

        if (goingDownData[i][0] > 0):
#            ConfigD[i] = ConfigD[i] - goingDownData[i][0]
            goingDownData[i][0] = 0

        for j in range(1,len(goingDownData[i])):
            goingDownData[i][j-1] = goingDownData[i][j]
           # ConfigD[i] = ConfigD[i] - goingDownData[i][j]
            goingDownData[i][j] = 0

        if (goingUpWeb[i][0] > 0):
#            ConfigW[i] = ConfigW[i] + goingUpWeb[i][0]
            goingUpWeb[i][0] = 0

        for j in range(1,len(goingUpWeb[i])):
            goingUpWeb[i][j-1] = goingUpWeb[i][j]
#            ConfigW[i] = ConfigW[i] + goingUpWeb[i][j]
            goingUpWeb[i][j] = 0

        if (goingUpJava[i][0] > 0):
#            ConfigJ[i] = ConfigJ[i] + goingUpJava[i][0]
            goingUpJava[i][0] = 0

        for j in range(1,len(goingUpJava[i])):
            goingUpJava[i][j-1] = goingUpJava[i][j]
#            if (i == 1 or i == 2):
#                ConfigJ[i] = ConfigJ[i] + goingUpJava[i][j]
            goingUpJava[i][j] = 0

        if (goingUpData[i][0] > 0):
#            ConfigD[i] = ConfigD[i] + goingUpData[i][j]
            goingUpData[i][0] = 0

        for j in range(1,len(goingUpData[i])):
            goingUpData[i][j-1] = goingUpData[i][j]
#            ConfigD[i] = ConfigD[i] + goingUpData[i][j]
            goingUpData[i][j] = 0


    #printArrays()

#parses cost data and stores it in the respective globals
def parseCost(data):
    global Revenue 
    global W_cost
    global J_cost
    global D_cost
    cost = data.split()
    Revenue = float(cost[1])/100
    W_cost = int(cost[2])
    J_cost = int(cost[3])
    D_cost = int(cost[4])
    print "REVENUE "+ str(Revenue)
    print "WEB " + str(W_cost)
    print "Java " + str(J_cost)
    print "Data " + str(D_cost)
    print ""

#calls the logic
def move():
    global J_cost
    global D_cost
    global Demand
    global secondProjArr
    global ConfigW
    global ConfigJ
    global ConfigD

    currentCapNW = float(ConfigW["NA"] * 190)
    currentCapEW = float(ConfigW["EU"] * 190)
    currentCapAW = float(ConfigW["AP"] * 190)
    currentCapNJ = float(ConfigJ["NA"] * 510)
    currentCapEJ = float(ConfigJ["EU"] * 510)
    currentCapAJ = float(ConfigJ["AP"] * 510)
    currentCapND = float(ConfigD["NA"] * 1200)
    currentCapED = float(ConfigD["EU"] * 1200)
    currentCapAD = float(ConfigD["AP"] * 1200)

    projND = calcDemand("NA",Demand)
    projED = calcDemand("EU",Demand)
    projAD = calcDemand("AP",Demand)

    #projected values for the first 6 turns before they are instantiated will be set as proj1
    projND2 = projND;
    projED2 = projED;
    projAD2 = projAD;
    projND3 = projND;
    projED3 = projED;
    projAD3 = projAD;

    #creates an array with the tail of Demand with the 3 projected demands appended to the end
    if(len(Demand) == 6):
        secondProjArr = projDemand(Demand,projND,projED,projAD)
        projND2 = calcDemand("NA",secondProjArr)
        projED2 = calcDemand("EU",secondProjArr)
        projAD2 = calcDemand("AP",secondProjArr)        
        thirdProjArr = projDemand(secondProjArr,projND2,projED2,projAD2)
        projND3 = calcDemand("NA",thirdProjArr)
        projED3 = calcDemand("EU",thirdProjArr)
        projAD3 = calcDemand("AP",thirdProjArr)

    control = []
    #Web NA
    control.append(webLogic(projND, projND2, projND3, currentCapNW, "NA"))
    #Web EU
    control.append(webLogic(projED, projED2, projED3, currentCapEW, "EU"))
    #Web AP
    control.append(webLogic(projAD, projAD2, projAD3, currentCapAW, "AP"))
    #Java NA
    control.append(javaLogic(projND, projND2, projND3, currentCapNJ, "NA"))
    #Java EU
    control.append(javaLogic(projED, projED2, projED3, currentCapEJ, "EU"))
    #Java AP
    control.append(javaLogic(projAD, projAD2, projAD3, currentCapAJ, "AP"))
    #Data NA
    control.append(dataLogic(projND, projED, projAD))

    val = "CONTROL"
    for i in range(len(control)):
        val += " "
        val += str(control[i])
        #val += str(0)
    #val = "CONTROL 0 0 0 0 0 0 0 -1 0"
    print val
    return val

#adds projected values into a copy of Demand called demandArray
def projDemand(arr,projND,projED,projAD):
    global secondProjArr
    for i in range (5):
        secondProjArr[i] = arr[i+1]
    secondProjArr[5] = {"NA": projND, "EU": projED, "AP": projAD}
    return secondProjArr

#calculates potential Damand change
#detects the trend by looking how long we have been rising or falling
def calcDemand(region,projDemand):
    global Demand
    global secondProjArr
    #doesn't start considering until we have at least 3 points
    if(len(projDemand) < 3):
        return projDemand[len(projDemand) - 1][region]

    i = 0
    dx = projDemand[len(projDemand) - 1][region] - projDemand[len(projDemand) - 2][region]
    if(dx > 0):
        trend = "up"
    else:
        trend = "down"
    for m in xrange(len(projDemand) - 2, 0, -1):
        i = i+1
        dx2 = projDemand[i][region] - projDemand[i - 1][region]
        if(dx > dx2):
            if(trend != "up"):
                return changeDemand(i, trend, region)
        if(dx < dx2):
            if(trend != "down"):
                return changeDemand(i, trend, region)

    return changeDemand(i, trend, region)


#does the math for calcDemand
def changeDemand(i, trend, region):
    global Demand
    current = Demand[len(Demand) - 1][region]
    dx = Demand[len(Demand) - 1][region] - Demand[len(Demand) - 2][region]
    dx2 = Demand[len(Demand) - 2][region] - Demand[len(Demand) - 3][region]

    if(dx * dx2 < 0 and abs(dx) > 90):
        if(dx > 0):
            return current + int(1.125 * dx)
        else:
            return current - int(1.125 * dx)

    if(i == 1):
        return current

    if(i == 2):
        if(trend == "up"):
            if(dx > 0):
                return current + int(1.125 * dx)
            else:
                return current - int(.5 * dx)
        else:
            if (dx < 0):
                return current - int(1.125 * dx)
            else:
                return current + int(.5 * dx)

    if(i == 3):
        if(trend == "up"):
            if(dx > 0):
                return current + int(1.25 * dx)
            else:
                return current - int(.25 * dx)
        else:
            if(dx < 0):
                return current - int(1.25 * dx)
            else:
                return current + int(.25 * dx)

    if(i == 4):
        if(trend == "up"):
            if(dx > 0):
                return current + int(1.5 * dx)
            else:
                return current - (.125 * dx)
        else:
            if (dx < 0 ):
                return current - int(1.5 * dx)
            else:
                return current + int(.125 * dx)

#Decisions on Web Servers
def webLogic(proj, proj2, proj3, cap, region):
    global Revenue
    global W_cost
    global goingUpWeb
    global goingDownWeb
    global ConfigW
    
    val = int(math.floor(proj - cap)/190)
    val2 = int(math.floor(proj2 - cap)/190)

    val3 = int(math.floor(proj3 - cap)/190)

    if(ConfigW[region] + val <= 0):
        return (-1*ConfigW[region] + 1)

#replaced val2 with val
    if(val > 0):
        #checks for previous changes
        for i in range(0, 2):
            if (goingUpWeb[region][i] != 0):
                return 0

        goingUpWeb[region][2] = val
    return val

#Decisions on Java Servers
def javaLogic(proj, proj2, proj3, cap, region):
    global Revenue
    global J_cost
    global goingUpJava
    global goingDownJava
    global ConfigJ
    global DistJ

    overflowRatio = {"NA": ("EU", 0.9), "EU": ("NA", 0.9), "AP": ("NA", 0.8)}
    overflow = Revenue*overflowRatio[region][1]*(proj - cap)
    addServer = Revenue*(proj - cap) - (J_cost + (1*J_cost))

    #considers if it is worth it to bother adding a server

    if(addServer < overflow):
        val = int(math.floor(proj - cap)/510)
        val2 = int(math.floor(proj2 - cap)/510)
        val3 = int(math.floor(proj3 - cap)/510)
    else:
        val = 0
        val2 = 0
        val3 = 0

    if (ConfigJ[region] + val <= 0):
        return 0
#replaced val2 with val
    if (val > 0):
        #checks if being added yet
        for i in range(0, 5):
            if (goingUpJava[region][i] != 0):
                return 0
        goingUpJava[region][2] = val
    else:
        for i in range(0, 2):
            if (goingDownJava[region][i] != 0):
                return 0
        goingDownJava[region][1] = val
    return val

#Decisions on Databases
def dataLogic(projN, projE, projA):
    global Revenue
    global D_cost
    global goingUpData
    global goingDownData
    global ConfigD
    global ConfigJ
    global DistD
    global Demand

    #what code sends out depending on which region we turn on or off

    val = {"NA": "1 0 0", "EU": "0 1 0", "AP": "0 0 1"}
    negval = {"NA": "-1 0 0", "EU": "0 -1 0", "AP": "0 0 -1"}

    print "TOTAL AMOUNT OF DATABASES: " + str(ConfigD["NA"]) + " " + str(ConfigD["EU"]) + " " + str( ConfigD["AP"])


    if (ConfigJ["NA"] > ConfigD["NA"] * 2 and ConfigJ["NA"] > 1):
        #checks if being modified already
        for i in range(0, 9):
            if (goingUpData["NA"][i] > 0):
                return "0 0 0"

        print "ADDING TO NA"
        goingUpData["NA"][8] = 1
        return val["NA"]

    elif (ConfigJ["EU"] > ConfigD["EU"] * 2 and ConfigJ["EU"] > 1 ):
        #checks for previous changes
        for i in range(0, 9):
            if (goingUpData["EU"][i] > 0):
                return "0 0 0"

        print "ADDING TO EUROPE"
        goingUpData["EU"][8] = 1
        return val["EU"]

    elif (ConfigJ["AP"] > ConfigD["AP"] * 2 and ConfigJ["AP"] > 1 ):
        #Checks for previous changes
        for i in range(0, 9):
            if (goingUpData["AP"][i] > 0):
                return "0 0 0"

        print "ADDING TO ASIA"
        goingUpData["AP"][8] = 1
        return val["AP"]
    
    elif( (ConfigD["NA"] + ConfigD["EU"] + ConfigD["AP"]) > 1 and ((ConfigD["NA"] + ConfigD["EU"] + ConfigD["AP"]) * 1200) >  (1100 + DistD["NA"] + DistD["EU"] + DistD["AP"])):
        print "IN THE REMOVAL"

        #Checks if removal is happening already
        for r in goingDownData:
            for i in range(0,3):
                if(goingDownData[r][i] != 0):
                    return "0 0 0"

        region = min(DistD.iteritems(), key=operator.itemgetter(1))[0]
        #Checks if the first region has no databases
        if(ConfigD[region] == 0):
            #if so it selects the second options
            locations = {"NA": DistD["NA"], "EU" : DistD["EU"] , "AP" : DistD["AP"]}
            locations.pop(region)
            region = min(locations.iteritems(), key = operator.itemgetter(1))[0]
            #Checks if the second region has no databases
            if(ConfigD[region] == 0):
                locations.pop(region)
                #if so it uses the third and this will definitely have a database
                region = locations.keys()[0]
        
        print "REMOVING DATABASES AND TOOK FROM: " + region + " CAP: " + str( (ConfigD["NA"] + ConfigD["EU"] + ConfigD["AP"]) * 1200) + " Distr: " + str( 1100 + DistD["NA"] + DistD["EU"] + DistD["AP"])
        print ""
        goingDownData[region][2] = 1
        return negval[region]
    return "0 0 0"

#parses demand data and stores it in global Demand
#global Demand will later be used to predict future demand
def parseDemand(data):
    global Demand
    demand = data.split()
    demand.pop(0)
    #if the length of Demand is > threshold, pop off the oldest data point
    if(len(Demand) >= 6):
        Demand.pop(0)
        Demand[0] = Demand[1]
        Demand[1] = Demand[2]
        Demand[2] = Demand[3]
        Demand[3] = Demand[4]
        Demand[4] = Demand[5]
        Demand[5] = {"NA": int(demand[4]), "EU": int(demand[5]), "AP": int(demand[6])}
    else:
        Demand[len(Demand)] = {"NA": int(demand[4]), "EU": int(demand[5]), "AP": int(demand[6])}  
       
#Pretty prints Demand
def printDemand():
    for i in range (0, len(Demand)):
        print str(i) + ": { NA: " + str(Demand[i]["NA"]) + " EU: " + str(Demand[i]["EU"]) + " AP: " + str(Demand[i]["AP"]) + " }"

    print "length: " + str(len(Demand))

#Parse Distribution
def parseDist(data):
    global DistW
    global DistJ
    global DistD

    dist = data.split()
    dist.pop(0)
    DistW["NA"] = int(dist[0])
    DistW["EU"] = int(dist[1])
    DistW["AP"] = int(dist[2])
    DistJ["NA"] = int(dist[3])
    DistJ["EU"] = int(dist[4])
    DistJ["AP"] = int(dist[5])
    DistD["NA"] = int(dist[6])
    DistD["EU"] = int(dist[7])
    DistD["AP"] = int(dist[8])


#Stores our current number of servers in each region into Config
def parseConfig(data):
    global ConfigW
    global ConfigJ
    global ConfigD
    config = data.split()
    config.pop(0)
    ConfigW["NA"] = int(config[0])
    ConfigW["EU"] = int(config[1])
    ConfigW["AP"] = int(config[2])
    ConfigJ["NA"] = int(config[3])
    ConfigJ["EU"] = int(config[4])
    ConfigJ["AP"] = int(config[5])
    ConfigD["NA"] = int(config[6])
    ConfigD["EU"] = int(config[7])
    ConfigD["AP"] = int(config[8])

#Pretty prints all key-value pairs in Config
def printAllConfig():
    global ConfigW
    global ConfigJ
    global ConfigD
    
    for i in ["NA", "EU", "AP"]:
        print i + " Web: " + str(ConfigW[i]) + " \t" + i + " Java: " + str(ConfigJ[i]) + " \t" + i + " Data: " + str(ConfigD[i])

def main():
    towrite = open('data.txt', 'w')
    data = init()
    endnum = 1
    i = 0
    while (data != "END"):
        print "---------------TURN# " + str(i) + "----------------"
        parseConfig(data)
        print "NA : " + str(ConfigD["NA"])
        printAllConfig()
        s.send("RECD")
        #DEMAND
        data = s.recv(1024)
        print data
        parseDemand(data)
        #printDemand()
        s.send("RECD")
        #DIST
        data = s.recv(1024)
        print data
        parseDist(data)
        s.send("RECD")
        #PROFIT
        data = s.recv(1024)
        print data
        towrite.write(str(Demand[len(Demand) - 1]["NA"]) + "," + str(Demand[len(Demand) - 1]["EU"]) + "," + str(Demand[len(Demand) - 1]["AP"]) + "," + str(ConfigW["NA"]) + "," + str(ConfigW["EU"]) + "," + str(ConfigW["AP"]) + "," + str(ConfigJ["NA"]) + "," + str(ConfigJ["EU"]) + "," + str(ConfigJ["AP"]) + "," + str(ConfigD["NA"]) + "," + str(ConfigD["EU"]) + "," + str(ConfigD["AP"]) + "," + data[-2:]+ "\n")
        towrite.flush()
        passArrayTime()
        s.send(move())
        print ""
        #CONFIG
        data = s.recv(1024)
        print data
        #   Uncomment if you want to go forward a set amount of turns instead of it just blazing buy
        #if(endnum <= 2880 and i > endnum):
        #    endnum = i - 1 + int(raw_input("Run how many turns more? Enter 2880 to run til end\n"))
        #    if(endnum >= 2880):
        #        endnum = 2880
        i = i+1
    towrite.write("END")
    s.send("STOP")
    s.close()


main()
