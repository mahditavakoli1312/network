#!/usr/bin/env python2

# من  سورس کامل نزدم کد زیر از ادرس
# https://github.com/nicolargo/pythonarena/blob/master/ping/ping05.py
#  از ادرس هی انتخابی پینگ میگره


import time
import socket
import struct
import select
import random
import asyncore

ICMP_ECHO_REQUEST = 8  # on Solaris.

ICMP_CODE = socket.getprotobyname('icmp')
ERROR_DESCR = {
    1: ' باید در فرآیند های  root اجرا شود',
    10013: ' باید با دسترسی  ادمین اجرا شود'

}

__all__ = ['create_packet', 'do_one', 'verbose_ping', 'PingQuery']

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) / 2) * 2
    # print("\n\n\n"+str(count_to)+"\n\n\n")
    count = 0
    while count < count_to:
        # print("\n\n\n" + str(count) + "\n\n\n")
        this_val = ord(chr(source_string[count + 1])) * 256 + ord(chr(source_string[count]))
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def create_packet(id):
    header = struct.pack('BBHHH', ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = 192 * 'Q'
    my_checksum = checksum(header + bytes(data,encoding='utf8'))
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,socket.htons(my_checksum), id, 1)
    return header + bytes(data,encoding='utf8')


def do_one(dest_addr, timeout=1):

    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    except socket.error as e:
        if e.errno in ERROR_DESCR:

            raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
        raise
    try:
        host = socket.gethostbyname(dest_addr)
    except socket.gaierror:
        return

    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id)

    while packet:

        sent = my_socket.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]
    delay = receive_ping(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return delay


def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if ready[0] == []:  # Timeout
            return
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id:
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def verbose_ping(dest_addr, timeout, count=4):

    for i in range(count):
        print('ping {}...'.format(dest_addr))
        delay = do_one(dest_addr, timeout)
        if delay == None:
            print('failed. (Timeout within {} seconds.)'.format(timeout))
        else:
            delay = round(delay * 1000.0, 4)
            print('get ping in {} milliseconds.'.format(delay))
    print('')


class PingQuery(asyncore.dispatcher):
    def __init__(self, host, p_id, timeout=0.5, ignore_errors=False):

        asyncore.dispatcher.__init__(self)
        try:
            self.create_socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        except socket.error as e:
            if e.errno in ERROR_DESCR:
                raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
            raise
        self.time_received = 0
        self.time_sent = 0
        self.timeout = timeout

        self.packet_id = int((id(timeout) / p_id) % 65535)
        self.host = host
        self.packet = create_packet(self.packet_id)
        if ignore_errors:
            self.handle_error = self.do_not_handle_errors
            self.handle_expt = self.do_not_handle_errors

    def writable(self):
        return self.time_sent == 0

    def handle_write(self):
        self.time_sent = time.time()
        while self.packet:

            sent = self.sendto(self.packet, (self.host, 1))
            self.packet = self.packet[sent:]

    def readable(self):
        if (not self.writable()

                and self.timeout < (time.time() - self.time_sent)):
            self.close()
            return False
        return not self.writable()

    def handle_read(self):
        read_time = time.time()
        packet, addr = self.recvfrom(1024)
        header = packet[20:28]
        type, code, checksum, p_id, sequence = struct.unpack("bbHHh", header)
        if p_id == self.packet_id:

            self.time_received = read_time
            self.close()

    def get_result(self):
        if self.time_received > 0:
            return self.time_received - self.time_sent

    def get_host(self):
        return self.host

    def do_not_handle_errors(self):
        pass

    def create_socket(self, family, type, proto):
        sock = socket.socket(family, type, proto)
        sock.setblocking(0)
        self.set_socket(sock)

        self.family_and_type = family, type

    def handle_connect(self):
        pass

    def handle_accept(self):
        pass

    def handle_close(self):
        self.close()


if __name__ == '__main__':
    time_out = input("enter timeout")
    time_out = int(time_out)

    string = input("enter string")
    split_string = string.split()

    for temp in split_string:
        verbose_ping(temp, time_out)

