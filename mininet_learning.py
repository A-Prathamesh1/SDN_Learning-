""" SOME LEARNING OUTCOMES
>>>Linear Network consisting of N > 2 nodes have 2n-n trees, n is number of nodes.

>>>In a tree network there are no loops and as in trees a path is link between the 
two nodes there can be only one path in two nodes.

>>>Capacity of path gets limited by the less capacity link in between the nodes.

>>>When we need to assign VLANS to different trees, we need to make sure 
no two trees share same links, as collisions needs to be avoided.

"""

""" Heres how would you check the versions """
import sys
print(sys.version)
import networkx
print(networkx.__version__)
import numpy as np
print(np.__version__)

""" 
 Mininet is Python based. In fact you can control all aspects of Mininet from Python.
 From a terminal to your Mininet VM use the command sudo python. 
 This brings up the Python interpreter as superuser which is needed since Mininet 
 creates network interfaces and such in the VM. At the Python command line enter the 
 code below to create, run, and test a very simple network
"""
 
from mininet.net import Mininet
from mininet.topo import Topo
topo = Topo()  # Create an empty topology
topo.addSwitch("s1")  # Add switches and hosts to the topology
topo.addHost("h1")
topo.addHost("h2")
topo.addLink("h1", "s1") # Wire the switches and hosts together with links
topo.addLink("h2", "s1")
net = Mininet(topo)  # Create the Mininet, start it and try some stuff
net.start()
net.pingAll()
net.iperf()
net.stop()

"""
Enter the following code into the Python interpreter (sudo python) running on your Mininet VM.
Does the a ping test between hosts work for you? Why or why not? Note that the default controller 
for the switches in Mininet implements an Ethernet learning bridge but does not support the spanning 
tree protocol.
Ping test between hosts dosent work, because there is loop in the network topology, the packetes 
are not finding their way through they are just bouncing between the routers.
"""

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink  # So we can rate limit links
from mininet.cli import CLI  # So we can bring up the Mininet CLI
topo = Topo()  # Create an empty topology
topo.addSwitch("s1")  # Add switches and hosts to the topology
topo.addSwitch("s2")
topo.addSwitch("s3")
topo.addHost("h1")
topo.addHost("h2")
topo.addHost("h3")
# Wire the switches and hosts together. Note there is a loop!
topo.addLink("h1", "s1", bw=20.0, delay='10ms', use_htb=True)
topo.addLink("h2", "s2", bw=25.0, delay='10ms', use_htb=True)
topo.addLink("h3", "s3", bw=25.0, delay='10ms', use_htb=True)
topo.addLink("s1", "s2", bw=11.0, delay='40ms', use_htb=True)
topo.addLink("s1", "s3", bw=15.0, delay='7ms', use_htb=True)
topo.addLink("s2", "s3", bw=5.0, delay='7ms', use_htb=True)
net = Mininet(topo=topo, link=TCLink)
net.start()
CLI(net)  # Bring up the mininet CLI
net.stop()

