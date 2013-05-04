#Team Midas
import socket

Revenue = 0
W_cost = 0
J_cost = 0
D_cost = 0

#Create the socket and connect to game server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("hackathon.hopto.org", 27832))
s.send("INIT Midas")

#ACCEPT
data = s.recv(1024)
print data
s.send("RECD")
#COSTS - R W J D
print data
s.send("START")
#CONFIG - W.na W.eu W.ap J.na J.eu. J.ap D.na D.eu D.ap
data = s.recv(1024)
print data

#while (data != "END"):
'''
for i in xrange(0,5):
    s.send("RECD")
    data = s.recv(1024)
    print data
    s.send("RECD")
    data = s.recv(1024)
    print data
    s.send("RECD")
    data = s.recv(1024)
    print data
    s.send("CONTROL 0 0 0 0 0 0 0 0 0")
    data = s.recv(1024)
    print data
'''
s.send("STOP")

print "\nENDED"
