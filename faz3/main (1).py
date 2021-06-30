#!/usr/bin/env python3

# dar in faz az github estefade kardam https://gist.github.com/pklaus/856268
import socket;
import struct;
import random;
import time;
import select;


ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp');

"""
bedast avordan checksum.
methodesh az jaee bardashtam motmaeen nistam
"""
def checksum(source_string):
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = (source_string[count + 1])*256 + (source_string[count])
        sum = sum + this_val
        sum = sum & 0xffffffff # Necessary?
        count = count + 2
    if count_to < len(source_string):
        sum = sum + (source_string[len(source_string) - 1])
        sum = sum & 0xffffffff # Necessary?
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


"""
sakhtan packet ba id moshakhas
"""
def create_packet(id):
    # type (8)byte , code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = ''
    # checksum ra baraye  data va  header packet test khodmon bedast miarim.
    my_checksum = checksum(header + data.encode('utf-8'))
    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
            socket.htons(my_checksum), id, 1)
    return header + data.encode('utf-8')


"""
ping migire agar timeout 0 agar movafaq meqdar ping ra bar mi gardune
baste bar asas id mifreste va ba 8 byte akhar ke header hast id check mikone
agar yeki bood zaman ping bedast miare
"""
def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if ready[0] == []: # Timeout
            return 0
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        # 8 byte akhar header packet hast
        icmp_header = rec_packet[-8:]
        type, code, checksum, p_id, sequence = struct.unpack(
                'bbHHh', icmp_header)
        #agar hamon baste boof(bar asas id) meqdar zaman ping bdast miare
        if p_id == packet_id:
            total_time_ms = (time_received - time_sent) * 1000
            # gerd kardan
            # total_time_ms = math.ceil(total_time_ms * 1000) / 1000
            return (addr[0], total_time_ms)
        time_left -= time_received - time_sent
        if time_left <= 0:
            return 0


"""
yek packet dorost mikone va ping migire va ttl ra dar header un pavket tanzim mikone 
agar timeout rohk dad 0 mikone va agar ok bood ping bar migardune
"""
def echo_one(host, ttl):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    my_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)


    #yek packet dorost mikone va mifreste

    packet_id = int(random.random() * 65535)
    packet = create_packet(packet_id)
    while packet:
        # The icmp protocol does not use a port, but the function
        # below expects it, so we just give it a dummy port.
        sent = my_socket.sendto(packet, (host, 1))
        packet = packet[sent:]

    ping_res = receive_ping(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return ping_res



""" 
    in method 3 bar echo_three ra seda mizanad lineE misazad ke natayeg ping ha tosh hast va hop ha
     va destination_reached ra meqdar mide agar true bashad yani ip addE ke req zadim behesh ba host match ast.

"""
def echo_three(host, ttl):
    try1 = echo_one(host, ttl)
    try2 = echo_one(host, ttl)
    try3 = echo_one(host, ttl)

    if try1 == 0:
        try1str = '*'
    else:
        try1str = try1[0] + ' - ' + str(try1[1]) + ' ms'
    if try2 == 0:
        try2str = '*'
    else:
        try2str = try2[0] + ' - ' + str(try2[1]) + ' ms'
    if try3 == 0:
        try3str = '*'
    else:
        try3str = try3[0] + ' - ' + str(try3[1]) + ' ms'

    final_string = try1str + ', ' + try2str + ', ' + try3str
    final_string = str(ttl) + '  ' + final_string

    if try1 == 0:
        destination_reached = False
    else:
        destination_reached = try1[0] == host

    return (final_string, destination_reached)



# -------------------------- #
# Main execution starts here #
# -------------------------- #

# if len(sys.argv) <= 1:
#     print('Bad usage. Provide a hostname.')
#     sys.exit(1)


dest_addr = input("enter dest addr >>")
#max_tries = input("enter max_tries >>")
#max_tries = int(max_tries)

timeout   = input("enter timeout>>")
timeout   = int(timeout)

maxTTl    = input("enter max ttl>>")
maxTTl    = int(maxTTl)

initTTl   = input("enter init ttl>>")
initTTl    = int(initTTl)

max_tries = maxTTl ;

#daryaft ip add from domain name
host = socket.gethostbyname(dest_addr)

#elam shoro
print('TraceRoute to ' + dest_addr + ' (' + host + '), ' + str(maxTTl) +
      ' hops max with 3 try.')
#done done ttl ha ra toye socket mizare albate dakhel echo_one
try:

    for x in range(initTTl, maxTTl+1):
        #baraye har hop 3 bar try mikone va natige 3 bar tyr ra baraye har hop dar yek khat neshon mide
        (line, destination_reached) = echo_three(host, x)
        print(line)
        #destination_reached baresi mikonad ke aya domain va host matchand ya na
        if destination_reached:
            break
except Exception as err:
    print(err)
except KeyboardInterrupt as err:
    print(err)