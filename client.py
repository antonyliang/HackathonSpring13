#Team Midas
import socket
import math

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
ConfigW = {}
ConfigJ = {}
ConfigD = {}

foo = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creates a connection to the game server and starts the game
def init():
    initArrays()
    global s
    s.connect(("hackathon.hopto.org", 27832))
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
            ConfigJ[i] = ConfigJ[i] - goingDownJava[i][0]
            goingDownJava[i][0] = 0

        for j in range(1,len(goingDownJava[i])):
            goingDownJava[i][j-1] = goingDownJava[i][j]
            goingDownJava[i][j] = 0

        if (goingDownData[i][0] > 0):
            ConfigD[i] = ConfigD[i] - goingDownData[i][0]
            goingDownData[i][0] = 0

        for j in range(1,len(goingDownData[i])):
            goingDownData[i][j-1] = goingDownData[i][j]
            goingDownData[i][j] = 0

        if (goingUpWeb[i][0] > 0):
            ConfigW[i] = ConfigW[i] + goingUpWeb[i][0]
            goingUpWeb[i][0] = 0

        for j in range(1,len(goingUpWeb[i])):
            goingUpWeb[i][j-1] = goingUpWeb[i][j]
            goingUpWeb[i][j] = 0

        if (goingUpJava[i][0] > 0):
            ConfigJ[i] = ConfigJ[i] + goingUpJava[i][0]
            goingUpJava[i][0] = 0

        for j in range(1,len(goingUpJava[i])):
            goingUpJava[i][j-1] = goingUpJava[i][j]
            goingUpJava[i][j] = 0

        if (goingUpData[i][0] > 0):
            ConfigD[i] = ConfigD[i] + goingUpData[i][0]
            goingUpData[i][0] = 0

        for j in range(1,len(goingUpData[i])):
            goingUpData[i][j-1] = goingUpData[i][j]
            goingUpData[i][j] = 0

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
    global ConfigW
    global ConfigJ
    global ConfigD

    currentCapNW = float(ConfigW["NA"] * 180)
    currentCapEW = float(ConfigW["EU"] * 180)
    currentCapAW = float(ConfigW["AP"] * 180)
    currentCapNJ = float(ConfigJ["NA"] * 450)
    currentCapEJ = float(ConfigJ["EU"] * 450)
    currentCapAJ = float(ConfigJ["AP"] * 450)
    currentCapND = float(ConfigD["NA"] * 1100)
    currentCapED = float(ConfigD["EU"] * 1100)
    currentCapAD = float(ConfigD["AP"] * 1100)

    projND = calcDemand("NA")
    projED = calcDemand("EU")
    projAD = calcDemand("AP")

    control = []
    #Web NA
    control.append(webLogic(projND, currentCapNW, "NA"))
    #Web EU
    control.append(webLogic(projED, currentCapEW, "EU"))
    #Web AP
    control.append(webLogic(projAD, currentCapAW, "AP"))
    #Java NA
    control.append(javaLogic(projND, currentCapNJ, "NA"))
    #Java EU
    control.append(javaLogic(projED, currentCapEJ, "EU"))
    #Java AP
    control.append(javaLogic(projAD, currentCapAJ, "AP"))
    #Data NA
    control.append(dataLogic(projND, currentCapND, "NA"))
    #Data EU
    control.append(dataLogic(projED, currentCapED, "EU"))
    #Data AP
    control.append(dataLogic(projAD, currentCapAD, "AP"))

    val = "CONTROL"
    for i in range(len(control)):
        val += " "
        val += str(control[i])
        #val += str(0)
    #val = "CONTROL 0 0 0 0 0 0 0 -1 0"
    print val
    return val


#calculates potential Damand change
#detects the trend by looking how long we have been rising or falling
def calcDemand(region):
    global Demand
    #doesn't start considering until we have at least 3 points
    if(len(Demand) < 3):
        return Demand[len(Demand) - 1][region]

    i = 0
    dx = Demand[len(Demand) - 1][region] - Demand[len(Demand) - 2][region]
    if(dx > 0):
        trend = "up"
    else:
        trend = "down"
    for m in xrange(len(Demand) - 2, 0, -1):
        i = i+1
        dx2 = Demand[i][region] - Demand[i - 1][region]
        if(dx > dx2):
            if(trend != "up"):
                return changeDemand(i, trend, region)
        if(dx < dx2):
            if(trend != "down"):
                return changeDemand(i, trend, region)

    return changeDemand(i, trend, region)

#does the math for calcDemand
def changeDemand(i, trend, region):
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
            return current + int(1.125 * dx)
        else:
            return current - int(1.125 * dx)

    if(i == 3):
        if(trend == "up"):
            return current + int(1.25 * dx)
        else:
            return current - int(1.25 * dx)

    if(i == 4):
        if(trend == "up"):
            return current + int(1.5 * dx)
        else:
            return current - int(1.5 * dx)

#Decisions on Web Servers
def webLogic(proj, cap, region):
    global Revenue
    global W_cost
    global goingUpWeb
    global goingDownWeb
    global ConfigW

    val = int(math.ceil(proj - cap)/180)
    if(ConfigW[region] + val <= 0):
        return 0

    if (val > 0):
        goingUpWeb[region][2] = val
    return val

#Decisions on Java Servers
def javaLogic(proj, cap, region):
    global Revenue
    global J_cost
    global goingUpJava
    global goingDownJava
    global ConfigJ

    #Weigh servers vs overflow
    overflowRatio = {"NA": ("EU", 0.9), "EU": ("NA", 0.9), "AP": ("NA", 0.8)}
    overflow = Revenue*overflowRatio[region][1]*(proj - cap)
    addServer = Revenue*(proj - cap) - (J_cost + (1*J_cost))

#    print str(proj-cap)
#    print str(region)
    print "overflow: " + str(overflow)
    print "addServer: " + str(addServer)

    if(addServer < overflow):
        val = int(math.ceil(proj - cap)/450)
    else:
        val = 0

    if (ConfigJ[region] + val <= 0):
        return 0

    if (val > 0):
        goingUpJava[region][2] = val
    else:
        goingDownJava[region][1] = val
    return val

#Decisions on Databases
def dataLogic(proj, cap, region):
    global Revenue
    global D_cost
    global goingUpData
    global goingDownData
    global ConfigD

    #Weigh servers vs overflow
    overflowRatio = {"NA": ("EU", 0.9), "EU": ("NA", 0.9), "AP": ("NA", 0.9)}
    overflow = Revenue*overflowRatio[region][1]*(proj - cap)
    addServer = Revenue*(proj - cap) - (D_cost + (2*D_cost))
    if(addServer < overflow):
        val = int(math.ceil(proj - cap)/1100)
    else:
        val = 0

#    val = int(math.ceil(proj - cap)/1100)
    if(ConfigD[region] + val <= 0):
        return 0

    if (val > 0):
        goingUpData[region][8] = val
    else:
        goingDownData[region][2] = val
    return val

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
    

#Pretty prints a key-value pair in Config
#x is the tier.region you're looking for
#e.g. printConfig("W.na") prints the number of servers in the Web tier of North America
#case-sensitive
def printConfigW(x):
    print x + ": " + ConfigW[x]

def printConfigJ(x):
    print x + ": " + ConfigJ[x]

def printConfigD(x):
    print x + ": " + ConfigD[x]

#Pretty prints all key-value pairs in Config
def printAllConfig():
    global ConfigW
    global ConfigJ
    global ConfigD
    
    for i in ["NA", "EU", "AP"]:
        print i + " Web: " + str(ConfigW[i]) + " \t" + i + " Java: " + str(ConfigJ[i]) + " \t" + i + " Data: " + str(ConfigD[i])

def main():
    data = init()
    endnum = 1
    i = 0
#    while (data != "END"):
    while (i < 2880):
        print "---------------TURN# " + str(i) + "----------------"
        parseConfig(data)
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
        s.send("RECD")
        #PROFIT
        data = s.recv(1024)
        print data
        passArrayTime()
        s.send(move())
        print ""
        #CONFIG
        data = s.recv(1024)
        #print data
        if(endnum <= 2880 and i > endnum):
            endnum = i - 1 + int(raw_input("Run how many turns more? Enter 2880 to run til end\n"))
            print "CURRENT ENDNUM"
            print endnum
            if(endnum >= 2880):
                endnum = 2880
        i = i+1
    s.send("STOP")
    s.close()


main()

print "\nENDED"
