"""
# Creating the Paths via OpenFlow
We need to find graph from your network and two nodes, say A and B,
which are connected by a link and gives the port that one would take
to get from node A to node B

"""
def out_port(a,b,g):
    edege = g.get_edge_data(a,b)
    if edege == None:
        print(f"Nodes [a] and [b] are not connected ")
        return None
    return edege["ports"][a] # returns the ports that host is connected to switch

out_port("H12","S1",g)

"""
To allow us to set up specific paths we need to match on both source and 
destination Ethernet addresses
"""
match = {"de_src": "source ether address", "dl_dst": "ether dest address"}
g.node["H11"]["mac"]

"""
Python function to setup a given path using the Ryu REST interface, matching 
on source and destination address. This function will need to take the path as 
a list of nodes, the network graph, and a mapping between switch names and DPIDs.
"""

def setup_path(path, g, name_dpid=None):
    src = g.node[path[0]]["mac"]
    dst = g.node[path[-1]]["mac"]
    print(f"sources: {src}, Dest: {dst}")
    for i in range(1, len(path)-1):
        print(f"switch {path[i]} uses port { out_port(path[i], path[i+1],g)}")
        if name_dpid != None:
            #send off requests
             msg = {  # Forwarding table entry and switch information
                "dpid": name_dpid[path[i]],   # Switch number here
                "cookie": 1,
                "cookie_mask": 1,
                "table_id": 0,
                "idle_timeout": 0,  # Doesn't idle time out
                "hard_timeout": 0,  # Doesn't hard time out
                "priority": 11111,
                "flags": 1,
                "match":{ "dl_src":src,  "dl_dst":dst }, ## Matches anything packet arriving on any port
                "actions":[
                    {
                    "type":"OUTPUT",
                    "port": out_port(path[i],path[i+1],g) # Floods out of all the ports except what it came in on
                    }
                ]
                }
             r = requests.post("http://127.0.0.1:8080/stats/flowentry/add", json=msg)    
             print(f" status code {r.status_code}, response  {r.text}")

print(wpath)
setup_path(wpath,g)