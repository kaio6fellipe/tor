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