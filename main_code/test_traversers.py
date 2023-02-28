from PyHugeGraph import PyHugeGraphClient
from helper.traversers import traversers
from helper.read_data import read_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_100000")

print(traversers.traverser_shortest_path(hg, source="1:1", target="1:4", max_depth=10000))
# print(traversers.traverser_kout(hg, source="1:1", max_depth=10))

print(traversers.traverser_kout(hg, source="1:1", max_depth=5))
print(traversers.traverser_kneighbor(hg, source="1:50000", max_depth=3))