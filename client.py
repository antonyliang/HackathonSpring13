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

#parses demand data and stores it in global Demand
#global Demand will later be used to predict future demand
def parseDemand(data):
    global Demand
    demand = data.split()
    demand.pop(0)
    Demand.append(("Date", demand[0] + " " + demand[1] + ":" + demand[2] + ":" + demand[3]))
    Demand.append(("Demand", ("NA", demand[4]), ("EU", demand[5]), ("AP", demand[6])))
#    print "Demand: " + str(Demand)



#while (data != "END"):
def main():
    init()
    for i in xrange(0,5):
        #DEMAND
        s.send("RECD")
        data = s.recv(1024)
        print data
        parseDemand(data)
        #DIST
        s.send("RECD")
        data = s.recv(1024)
        print data
        #PROFIT
        s.send("RECD")
        data = s.recv(1024)
        print data
        #CONFIG
        s.send("CONTROL 0 0 0 0 0 0 0 0 0")
        data = s.recv(1024)
        print data
    s.send("STOP")

main()

print "\nENDED\n"
