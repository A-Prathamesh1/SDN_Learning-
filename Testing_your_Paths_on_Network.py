"""
 Create a mapping between switch names and DPIDs.
"""
import requests
r = requests.get("http://127.0.0.1:8080/stats/switches") 
dpids = r.json()  # Gets DPIDs as a list of integers, but we only know them by name.
# Let's create a map from switch name to data path ids (dpid)
name_id = {}
for dpid in dpids: # converting name to number and we need to be able to do revers (numbers to names ana vice versa)
    my_bytes = (dpid).to_bytes(4, 'big') # Break integer into bytes
    name = my_bytes.decode('utf8').lstrip('\x00') # Convert bytes to UTF-8 string w/o junk
    name_id[name] = dpid
print(name_id) #{}

# Obtained from long all simple path calculation and storing it in list
long_path = ['H11', 'S1', 'S7', 'S8', 'S6', 'S5', 'S9', 'S2', 'S10', 'S3', 'S11', 'S4', 'H42']
print(f"Longest path{long_path} length{ len(long_path)}")
print(f"Widest path{wpath} length:{len(wpath)}")
 
#set up the "longest path" 

setup_path(long_path,g)
# print(wpath)
# the_path = wpath[-1]
long_path.reverse()
print(f"\nReversing logest path : ")
setup_path(long_path,g)

#set up the "widest path"
setup_path(wpath,g)
wpath.reverse()
print(f"\nReversing wpath path :")
setup_path(wpath,g)