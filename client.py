#Team Midas
import socket

Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

def parseCost(data):
    global Revenue 
    global W_cost
    global J_cost
    global D_cost
    stuff = data.split()
    Revenue = int(stuff[1])
    W_cost = int(stuff[2])
    J_cost = int(stuff[3])
    D_cost = int(stuff[4])
    print "REVENUE "+ str(Revenue)
    print "WEB " + str(W_cost)
    print "Java " + str(J_cost)
    print "Data " + str(D_cost)

def move():
    if (True):
        return "CONTROL 0 0 0 0 0 0 0 0 0"

def main():
    init()
    data = ""
    while (data != "END"):
        s.send("RECD")
        data = s.recv(1024)
        print data
        s.send("RECD")
        data = s.recv(1024)
        print data
        s.send("RECD")
        data = s.recv(1024)
        print data
        s.send(move())
        data = s.recv(1024)
        print data
    s.send("STOP")

main()

print "\nENDED"
