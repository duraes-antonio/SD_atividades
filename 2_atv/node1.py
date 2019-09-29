import time

from pyp2p.net import *

# Setup Alice's p2p node.
alice = Net(
	passive_bind="192.168.1.101", passive_port=44444,
	interface="wlx00266601ac4d:1", node_type="passive", debug=1)
alice.start()
alice.bootstrap()
alice.advertise()

# Event loop.
while 1:
	for con in alice:
		for reply in con:
			print(reply)

	time.sleep(1)
