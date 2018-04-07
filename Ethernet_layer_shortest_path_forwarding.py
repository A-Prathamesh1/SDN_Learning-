"""
>>> You will need a copy of the OpenFlow Switch Specification 1.0.0 and 
the IEEE 802.1AB Station and Media Access Control Connectivity Discovery 
(LLDP) specification

>>>
"""
import networkx as nx
import json

# print the information on the number of nodes and switches

gnl = json.load(open("Anim_conf_Net.json"))# For demo only, this should be your network!
g = nx.json_graph.node_link_graph(gnl) #Returns node-link data format
print(f"number of nodes {g.number_of_nodes()}, number of edges: {g.number_of_edges()}")
print(f"Edges: {list(g.edges(data=False))}")

# NetworkX create a list of switch nodes and a list of host nodes

g.nodes(data=True)
switches = []
hosts = []
for n in g.nodes(): # for each node in graph-node format
    if(g.node[n]['type'] == 'switch'):
        switches.append(g.node[n])
        print(n,g.node[n]['type'])
    if(g.node[n]['type'] == 'host'):
        hosts.append(g.node[n])
        print(n,g.node[n]['type'])

# Create the switch to host mapping, i.e., lists of hosts associated with

nodes = g.nodes()
hosts = [n for n in nodes if g.node[n]['type'] == 'host'] #creating list of hosts and swiches
switches = [n for n in nodes if g.node[n]['type'] == 'switch'] #and swiches

switch_host_map = {} # an empty dictionary to store the switch_host_map
for s in switches:
    switch_host_map[s] = [] #empty list inside dictioary for each switch to store hosts
for h in hosts:
    hedges = list(g.edges(h)) # Modification for NetworkX 2.0
    if len(hedges) != 1:
        raise Exception("Hosts must be connected to only one switch in this model") # we are not using multihoming for now
    other = hedges[0][1]  # Should be the other side of the link
#     print(hedges[0][1])
    if not other in switches:
        raise Exception("Hosts must be connected only with a switch in this model")
    switch_host_map[other].append(h)  #Okay add the host to the switch map
print(switch_host_map)

# Computing Shortest path using networkX 

g_switches = g.subgraph(switches)
print("g_switches: {}".format(g_switches.nodes()))
print("g_switches has:{} swithces".format(g_switches.number_of_nodes()))

g_switches: ['S1', 'S2', 'S3', 'S4', 'S5']
spaths = nx.shortest_path(g_switches, weight='weight')
print(f"shortest path from s1 to s5",spaths)
print(f"is direceted:",{g_switches.is_directed()}) # is it direceted o

# Compute next hop port forwarding table for switches

next_hop_port = {}
for s_src in switches:# we go through all the source nodes and destination nodes. 
    for s_dst in switches:
        if s_src != s_dst:
            path = spaths[s_src][s_dst]
            next_hop = path[1]  # Get the next hop along path from src to dst
            port = g_switches.get_edge_data(s_src,next_hop)["ports"][s_src]
            next_hop_port[(s_src, s_dst)] = port
            print(next_hop_port[(s_src, s_dst)])  

cur_switch ='S2'
dst_switch ='S5'
port = next_hop_port[(cur_switch,dst_switch)]
print(f"the next egress port for {dst_switch} on {cur_switch} is port {port}")

#Create MAC to port forwarding table for each switch based on Switch to Switch forwarding

mac_fwd_table = {}
for s_src in switches:
    mac_fwd_table[s_src] = {}  # Initialize forwarding table for each source switch
    for s_dst in switches:
        if s_src != s_dst:
            for h in switch_host_map[s_dst]:
                h_mac = g.node[h]['mac']
                mac_fwd_table[s_src][h_mac] = next_hop_port[(s_src, s_dst)]
        else:  # Host is directly connected to the switch
            for h in switch_host_map[s_dst]:
                port = g.get_edge_data(s_src,h)["ports"][s_src]
                h_mac = g.node[h]['mac']
                mac_fwd_table[s_src][h_mac] = port
# return mac_fwd_table
ex_switch ='S3'
print(f"Forwarding table for switch {ex_switch}: {mac_fwd_table[ex_switch]}")

#Fill the flow tables of the switches with the forwarding information using the Ryu REST interface

import requests
r = requests.get("http://127.0.0.1:8080/stats/switches") #[21298, 21300, 21299, 21301, 21297] 
dpids = r.json()  # Gets DPIDs as a list of integers, but we only know them by name.

# Let's create a map from switch name to data path ids (dpid)

name_id = {}
for dpid in dpids: # converting name to number and we need to be able to do revers (numbers to names ana vice versa)
    my_bytes = (dpid).to_bytes(4, 'big') # Break integer into bytes
    name = my_bytes.decode('utf8').lstrip('\x00') # Convert bytes to UTF-8 string w/o junk
    name_id[name] = dpid
print(name_id) #{}

name_id = {}
for s in switches:
        print(f"switch: {s}")
        for dst, port in mac_fwd_table[s].items():
            msg = {  # Forwarding table entry and switch information
                "dpid": name_id[s],   # Switch number here
                "cookie": 1,
                "cookie_mask": 1,
                "table_id": 0,
                "idle_timeout": 0,  # Doesn't idle time out
                "hard_timeout": 0,  # Doesn't hard time out
                "priority": 11111,
                "flags": 1,
                "match":{ "dl_dst":dst# Matches anything packet arriving on any port
                },
                "actions":[
                    {
                    "type":"OUTPUT",
                    "port": port # Floods out of all the ports except what it came in on
                    }
                ]
                }
            r = requests.post("http://127.0.0.1:8080/stats/flowentry/add", json=msg)  
            print(f"status code: {r.status_code}, response: {r.text}")
        #for dst, port in mac_fwd_table[s].items():
         #   print(f"dest: {dst}, port: {port}")