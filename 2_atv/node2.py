from pyp2p.net import *

# Setup Bob's p2p node.
bob = Net(
	passive_bind="192.168.1.101", passive_port=44445,
	interface="wlx00266601ac4d:1", node_type="passive", debug=1)
bob.start()
bob.bootstrap()
bob.advertise()

# Event loop.
while 1:
	for con in bob:
		con.send_line("test")

	time.sleep(1)
