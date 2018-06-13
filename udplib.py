import socket


class UDP(object):
    """simple UDP ping class"""
    handle = None   # Socket for send/recv
    port = 0        # UDP port we work on
    address = ''    # Own address
    broadcast = ''  # Broadcast address

    def __init__(self, port, address=None, broadcast=None):
        if address is None:
            local_addrs = socket.gethostbyname_ex(socket.gethostname())[-1]
            for addr in local_addrs:
                if not addr.startswith('127'):
                    address = addr
        if broadcast is None:
            broadcast = '255.255.255.255'

        self.address = address
        self.broadcast = broadcast
        self.port = port
        # Create UDP socket
        self.handle = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Ask operating system to let us do broadcasts from socket
        self.handle.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def bind():
        # Bind UDP socket to local port so we can receive pings
        self.handle.bind(('', self.port))

    def send(self, buf):
        self.handle.sendto(buf, 0, (self.broadcast, self.port))

    def recv(self, n):
        buf, addrinfo = self.handle.recvfrom(n)
        if addrinfo[0] != self.address:
            print("Found peer %s:%d" % addrinfo)
        return buf



if __name__=="__main__":
    import time
    import pygame
    import numpy
    from pygame.locals import *
    pygame.init()

    over=False

    u=UDP(9000)
    cmd=b'\x00'
    clock = pygame.time.Clock()
    key=numpy.zeros(323)
    screen_width, screen_height = 600, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    while not over:
        clock.tick(60)
        key[:]=pygame.key.get_pressed()

        cmd=b''
        if key[K_w]:
            cmd+=b'w'
        if key[K_a]:
            cmd+=b'a'

        if key[K_s]:
            cmd+=b's'

        if key[K_d]:
            cmd+=b'd'

        if key[K_h]:
            cmd+=b'h'
        print(cmd)
        u.send(cmd)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               over=True

        

 

            