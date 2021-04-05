import socket
import threading
from queue import Queue
import time
import sys

print_lock = threading.Lock();

target = sys.argv[1]

def scan(port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(int(dtimeout))   
    try:
        con = s.connect((target,port))
        with print_lock:
            print('port ',port,'is open')
            con.close()
    except:
        pass
        
             
def threader():
    while True:
        worker = q.get()
        scan(worker)
        q.task_done()
        
q = Queue()

nthread = input("number of threads ?")
dtimeout = input("timeout?")
portrange = input("range is (1,?)")

for x in range(int(nthread)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
start = time.time()

Ports = [80,443,22,21,25,23]
for worker in range(1,int(portrange)):
    q.put(worker)
    
q.join()

















