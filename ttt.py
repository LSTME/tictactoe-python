#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

other = (1, 0)

class Game:
    def __init__(self, gid, pname, mover, server, port):
        self.server = server
        self.port = port
        self.gid = gid
        self.pname = pname
        self.mover = mover

    def send_utf8(self, s):
        self.socket.send(s.encode('utf8')+b'\n')

    def recv_utf8(self, b=1024):
        return self.socket.makefile().readline().strip()

    def run(self):
        self.socket = socket.socket()
        self.socket.connect((self.server, self.port))
        self.send_utf8(f"HELO {self.gid} {self.pname}")
        r = self.recv_utf8().split()
        assert r[0] == "OK"
        assert r[1] == self.gid
        n = int(r[2])
        self.cb = self.mover(n)
        pid = int(r[3])
        m = [0] * (n*n)
        def lin(x, y):
            return y*n+x
        def get(x, y):
            return m[y*n+x]
        while True:
            r = self.recv_utf8().split()
            if r[0] == "MOVE":
                x, y = map(int, r[1:])
                print(f"Received move to {x} {y}")
                if x != -1:
                    m[lin(x, y)] = 2
                mx, my = self.cb(get, x, y, x==-1)
                m[lin(mx, my)] = 1
                print(f"Sending move to {mx} {my}")
                self.send_utf8(f"MOVE {mx} {my}")
            elif r[0] == "GAMEEND":
                if int(r[1]) == -1:
                    print("Draw!")
                    return 0
                if int(r[1]) == -2:
                    print("Opponent disconnected!")
                    return 2
                print("You win!" if int(r[1]) == pid else "You lose!")
                return 0
            else:
                print(r)
                print("shit went wrong.")
                return -1

def mkmover(cb):
    class Mover:
        def __init__(self, n):
            self.n = n
        def __call__(self, get, x, y, first):
            cb(get, n, x, y, first)
    return Mover
