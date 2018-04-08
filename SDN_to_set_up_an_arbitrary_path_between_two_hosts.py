"""
SDN to set up an arbitrary path between any two host 
how use LLDP packets to discover hosts attached to switches.

Compute the k-shortest paths between those two nodes. to find
How many (simple) paths can you find between the two nodes
"""
# Non-Shortest Path Packet Routing, We don't usually do this but we need to check iperf for delay 
import networkx as nx
import json

gnl = json.load(open("meshy_network1.json"))# For demo only, this should be your network json file!
g = nx.json_graph.node_link_graph(gnl) #Returns node-link data format
#print(f"number of nodes {g.number_of_nodes()}, number of edges: {g.number_of_edges()}")
nodes = g.nodes()
print("nodes",nodes)

def pathCap(path, g, cap="capacity"):
    p_cap = float("inf")
    for i in range(len(path)-1):
        if not g.has_edge(path[i], path[i+1]):
            raise Exception('Bad Path')
        else:
            p_cap = min(p_cap, g[path[i]][path[i+1]][cap])
    if p_cap == float("inf"):
        p_cap = 0
    return p_cap

def pathCost(path, g, weight="weight"):
    p_cost = 0.0
    for i in range(len(path)-1):
        if not g.has_edge(path[i], path[i+1]):
            raise Exception('Bad Path')
        else:
            p_cost += g[path[i]][path[i+1]][weight]
    return p_cost

spaths = nx.shortest_simple_paths(g, source='H11', target='H42', weight='weight')#Calculating the shortest simple path H11 to H42
my_paths = []
my_path_lengths = []
for path in spaths:
    # comment following line 
    print(f"Cost :{pathCost(path,g)}, Cap: {pathCap(path,g)}, {path} has length:{len(path)}\n") 
    my_paths.append(path)
    my_path_lengths.append(len(path)) 

print(f"There are total {len(my_paths)} simple shortest path between, H11 and H42")
print(f"Longest path has length {max(my_path_lengths)}")

#we need to save widest path node names as string
wpath = ['H11','S1', 'S8', 'S9', 'S11', 'S4', 'H41']
print(f"Widest path has length of:{len(wpath)}")


