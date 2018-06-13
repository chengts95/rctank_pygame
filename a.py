from __future__ import print_function

import signal
import pyuv
import time
from multiprocessing import process
import sys

client=""

def on_read(handle, ip_port, flags, data, error):
    global client
    if data is not None:
        if client=="":
            client=ip_port
            print(client)

def signal_cb(handle, signum):

    server.close()
    tty_stdin.close()
    tty_stdout.close()
    
    signal_h.close()

def on_tty_read(handle, data, error):
    data=data[:-2]
    if data is None or data == b"exit":
        tty_stdin.close()
        tty_stdout.close()
        signal_h.close()
        server.close()
    else:
        server.send(client,data)

print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()

server = pyuv.UDP(loop)
server.bind(("0.0.0.0", 8080))
server.start_recv(on_read)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)
tty_stdin = pyuv.TTY(loop, sys.stdin.fileno(), True)
tty_stdin.start_read(on_tty_read)
tty_stdout = pyuv.TTY(loop, sys.stdout.fileno(), False)

if sys.platform != "win32":
    print("Window size: (%d, %d)" % tty_stdin.get_winsize())

loop.run()
pyuv.TTY.reset_mode()
print("Stopped!")