# tor

pip install requests
pip install requests[socks]
pip install requests[security]

pip install stem
sudo apt-get install tor
sudo service tor start

#Test Tor connection
#curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/ | cat | grep -m 1 Congratulations | xargs

sudo echo 'ControlPort 9051' >> /etc/tor/torrc
sudo echo 'CookieAuthentication 0' >> /etc/tor/torrc
