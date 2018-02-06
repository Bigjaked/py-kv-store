# -*- coding: utf-8 -*-


from persist_kv_store.stores import SqliteMemoryStore
import ujson
from server_config import *
from curio import run, spawn
from curio.socket import *

def serialize_stream(stream):
    return
async def kv_server(kv_store_instance):
    key_value_store = kv_store_instance()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((ADDRESS, PORT))
    server_socket.listen(5)
    async with server_socket:
        while True:
            (client_socket, client_address) = server_socket.accept()
            await spawn(kv_store_client, client_socket, client_address)

async def kv_store_client(client_sock, client_addr):
    async with client_sock:
        while True:
            data = await client_sock.recv(1000)
