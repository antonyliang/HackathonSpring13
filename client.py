#Team Midas
import socket

Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

def init():
    #Create the socket and connect to game server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("hackathon.hopto.org", 27832))
    s.send("INIT Midas")
    #ACCEPT
    data = s.recv(1024)
    print data
    s.send("RECD")
    data = s.recv(1024)
    print data

def parseCost(data):
    
    print "REVENUE "+ Revenue
    print "WEB " + W_cost
    print "Java " + J_cost
    print "Data " + D_cost

def parseConfig(data):
    config = data.split()
    config.pop(0)
    return config

def parseDemand(data):
    demand = data.split()
    demand.pop(0)
    return demand

def parseProfit(data):
    profit = data.split()
    profit.pop(0)
    return profit

print parseConfig("CONFIG 2 2 23 1 1 1 0 1 0")

#CONFIG - W.na W.eu W.ap J.na J.eu. J.ap D.na D.eu D.ap

#while (data != "END"):
'''
for i in xrange(0,1):
    #CONFIG
    s.send("RECD")
    data = s.recv(1024)
    print data
    #DEMAND
    s.send("RECD")
    data = s.recv(1024)
    print data
    #DIST
    s.send("RECD")
    data = s.recv(1024)
    print data
    #PROFIT
    s.send("CONTROL 0 0 0 0 0 0 0 0 0")
    data = s.recv(1024)
    print data
'''
print "\nENDED"
