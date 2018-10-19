#!/usr/bin/env python3


class ServerConfig:
    FLAG = False
    MAX_CONNS = 128
    BUFFER = 1024
    SHORT_INTERVAL = 0.1
    INTERVAL = 0.8
    MID_INTERVAL = 5
    LONG_INTERVAL = 10
    SIG = str.encode("ACTIVE")
    NONE_TIMEOUT = None

    def __init__(self):
        self._port = None
        self._loopback_conn = None
        self._plat = None
        self.choice = None
        self._plat = None

    # initializer
    def init_server_config(self):
        # set looper to receive all connections
        self._loopback_conn = "0.0.0.0"
        # set the port
        # self._port = 4434
        self._port = 8080