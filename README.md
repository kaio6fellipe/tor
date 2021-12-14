# Configuration
Install some Python packages:
```shell
pip install requests
```
```shell
pip install requests[socks]
```
```shell
pip install requests[security]
```
```shell
pip install stem
```

Install TOR:
```shell
sudo apt-get install tor
```
```shell
sudo service tor start
```

Testing the Tor connection:
```shell
curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs
```

Alter the torrc file:
```shell
sudo echo 'ControlPort 9051' >> /etc/tor/torrc
```
```shell
sudo echo 'CookieAuthentication 0' >> /etc/tor/torrc
```
# Details

The [tor.py](./tor.py) file contains 3 functions to use in your code: 

- StartConnection
- CloseConnectionProcess
- NewConnection

The StartConnection function will establish the connection to the tor network, returning 2 connection sockets (tor_socket and original_socket) and the new IP address.

The CloseConnectionProcess function will terminate the connection socket with the tor network, this function has 2 madatory parameters, the tor_socket and the original_socket must be passed to it.

The NewConnection function will do the process of closing an old connection and opening a new connection with the tor network, it has 2 madatory parameters (tor_socket and original_socket) and will return the new IP address with 2 connection sockets (tor_socket and original_socket).

# Example


```python
import requests
import tor
import socket

# Get the current IP address.
original_ip_address = requests.get('https://ident.me').text
print("Original address: %s " % original_ip_address)

# Start the Tor connection, returning the new IP address, the original socket and the tor socket, by default, the tor socket will already be active.
new_ip_addr, original_socket, tor_socket = tor.StartConnection()
print("New address: %s " % new_ip_addr)

# If you want to use the original socket, you can do this:
socket.socket = original_socket
print("Original socket request: %s " % requests.get('https://ident.me').text) # Return your real IP address
# After that, every connection that you will make, will use the original socket.

# If you want to use the tor socket, you can do this:
socket.socket = tor_socket
print("Tor socket request: %s " % requests.get('https://ident.me').text) # Return your Tor IP address
# After that, every connection that you will make, will use the tor socket.

# Reset the connection with Tor, returning the new IP address, the original socket and the tor socket.
new_ip_addr, original_socket, tor_socket = tor.NewConnection(original_socket = original_socket, tor_socket = tor_socket)
print("New address after reset: %s " % new_ip_addr)
```
This example will generate the following output:
```console
tor on  main via 🐍 v2.7.18 took 38s 
❯ /bin/python3 /home/kaio/Documentos/tor/example.py
Original address: XXX.XXX.XXX.XXX 
New address: 176.10.99.200 
Original socket request: XXX.XXX.XXX.XXX 
Tor socket request: 176.10.99.200 
New address after reset: 104.244.72.91 
```