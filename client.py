#Team Midas
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("hackathon.hopto.org", 27832))
s.send("Hello")
data = s.recv(1024)

print "lol"
