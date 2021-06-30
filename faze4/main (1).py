from scapy.all import *
import sys
from scapy.layers.l2 import *

classType = input("enter class type : ('A','B','C')")
add_input  = input("enter start ip ( format ex: 192.168.1.) : ")
finish_add = input("enter decimal  format ex: 255) : ")
timeoutt = input("enter timeout : ")

if(classType=='C'):
 for addr in range(1,255):
    ans = sr1(ARP(pdst = add_input+str(addr)),timeout = int(timeoutt) ,verbose = 0)
    if ans :
        print("host found "+add_input+str(addr))

if(classType=='B'):
    for addr1 in range(1, 255):
     for addr2 in range(1, 255):
         ans = sr1(ARP(pdst=add_input + str(addr1)+str(addr2)), timeout=int(timeoutt), verbose=0)
         if ans:
             print("host found " + add_input + str(addr1)+str(addr2))
if(classType=='C'):
  for addr1 in range(1, 255):
     for addr2 in range(1, 255):
      for addr3 in range(1, 255):
          ans = sr1(ARP(pdst=add_input + str(addr1)+str(addr2)+str(addr3)), timeout=int(timeoutt), verbose=0)
          if ans:
              print("host found " + add_input + str(addr1)+str(addr2)+str(addr3))
