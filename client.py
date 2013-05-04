#Team Midas
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("hackathon.hopto.org", 27832))
s.send("INIT {Team Midas}")
data = s.recv(2048)

print data

print "lol"
