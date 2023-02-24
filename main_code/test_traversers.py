from PyHugeGraph import PyHugeGraphClient
from helper.traversers import traversers

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_10")

print(traversers.traverser_shortest_path(hg, source="1:1", target="1:4"))
print(traversers.traverser_kout(hg, source="1:1", max_depth=2))
print(traversers.traverser_kout(hg, source="1:1", max_depth=1))
print(traversers.traverser_kneighbor(hg, source="1:1", max_depth=1))