import requests
import time
from stem import Signal
from stem.control import Controller
import socks
import socket
from rich.console import Console

def func_NewConnectionProcess(**kwargs):
    original_socket = kwargs.get('original_socket')
    tor_socket = kwargs.get('tor_socket')
    func_CloseConnectionProcess(original_socket = original_socket, tor_socket = tor_socket)
    new_ip_addr, original_socket, tor_socket = func_StartConnectionProcess()
    return new_ip_addr, original_socket, tor_socket
  
def func_NewConnection(**kwargs):
    original_socket = kwargs.get('original_socket')
    tor_socket = kwargs.get('tor_socket')
    console = Console()
    with console.status("[bold]TOR connection in progress...") as status:
        new_ip_addr, original_socket, tor_socket = func_NewConnectionProcess(original_socket = original_socket, tor_socket = tor_socket)
        return new_ip_addr, original_socket, tor_socket
      
def func_CloseConnectionProcess(**kwargs):
    original_socket = kwargs.get('original_socket')
    tor_socket = kwargs.get('tor_socket')
    tor_socket = None
    socks.setdefaultproxy(None)
    socket.socket = original_socket

def func_StartConnectionProcess():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password='password')
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        original_socket = socket.socket
        tor_socket = socks.socksocket
        socket.socket = tor_socket
        controller.signal(Signal.NEWNYM)
        time.sleep(controller.get_newnym_wait())
        new_ip_addr = requests.get('https://ident.me').text
        return new_ip_addr, original_socket, tor_socket
      
 def func_StartConnection():
    console = Console()
    with console.status("[bold]TOR connection in progress...") as status:
        new_ip_addr, original_socket, tor_socket = func_StartConnectionProcess()
        return new_ip_addr, original_socket, tor_socket
