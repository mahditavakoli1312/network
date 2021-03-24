'''
Created on Mar 24, 2021

@author: sazgar
'''
#Python code for simple port scanning

import socket #importing library

ip = socket.gethostbyname (socket.gethostname()) #getting ip-address of host

for port in range(65535):  
    socket.setdefaulttimeout(1)   #check for all available ports

    try:

        serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # create a new socket

        serv.bind((ip,port)) # bind socket with address
            
    except:

        print('[OPEN] Port open :',port) #print open port number

    serv.close() #close connection

#
# import pyfiglet
# import sys
# import socket
# from datetime import datetime
#
# ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
# print(ascii_banner)
#
# # Defining a target
# if len(sys.argv) == 2:
    #
    # # translate hostname to IPv4
    # target = socket.gethostbyname(sys.argv[1])
# else:
    # print("Invalid ammount of Argument")
    #
# # Add Banner
# print("-" * 50)
# print("Scanning Target: " + target)
# print("Scanning started at:" + str(datetime.now()))
# print("-" * 50)
#
# try:
    #
    # # will scan ports between 1 to 65,535
    # for port in range(1,65535):
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.setdefaulttimeout(1)
        #
        # # returns an error indicator
        # result = s.connect_ex((target,port))
        # if result ==0:
            # print("Port {} is open".format(port))
        # s.close()
        #
# except KeyboardInterrupt:
        # print("\n Exitting Program !!!!")
        # sys.exit()
# except socket.gaierror:
        # print("\n Hostname Could Not Be Resolved !!!!")
        # sys.exit()
# except socket.error:
        # print("\ Server not responding !!!!")
        # sys.exit()
