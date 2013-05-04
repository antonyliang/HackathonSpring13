#Team Midas
import socket

#Globals
Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

Demand = []
Profit = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#creates a connection to the game server and starts the game
def init():
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
    print data

#parses cost data and stores it in the respective globals
def parseCost(data):
    global Revenue 
    global W_cost
    global J_cost
    global D_cost
    cost = data.split()
    Revenue = int(cost[1])
    W_cost = int(cost[2])
    J_cost = int(cost[3])
    D_cost = int(cost[4])
    print "REVENUE "+ str(Revenue)
    print "WEB " + str(W_cost)
    print "Java " + str(J_cost)
    print "Data " + str(D_cost)

def move():
    if (True):
        return "CONTROL 0 0 0 0 0 0 0 0 0"

#parses demand data and stores it in global Demand
#global Demand will later be used to predict future demand
def parseDemand(data):
    global Demand
    demand = data.split()
    demand.pop(0)
    Demand.append(("Date", demand[0] + " " + demand[1] + ":" + demand[2] + ":" + demand[3]))
    Demand.append(("Demand", ("NA", demand[4]), ("EU", demand[5]), ("AP", demand[6])))

#pretty prints Demand
def printDemand():
    for i in range (0,len(Demand),2):
        print str(Demand[i]) + "\t" + str(Demand[i+1])

def main():
    init()
    data = ""
#    while (data != "END"):
    for i in xrange(0,20):
        s.send("RECD")
        #DATA
        data = s.recv(1024)
        print data
        parseDemand(data)
        s.send("RECD")
        #DIST
        data = s.recv(1024)
        print data
        s.send("RECD")
        #PROFIT
        data = s.recv(1024)
        print data
        s.send(move())
        #CONFIG
        data = s.recv(1024)
        print data
    s.send("STOP")
    s.close()

main()


print "\nENDED"
