from PyHugeGraph import PyHugeGraphClient
from traversers import traversers

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_10")

print(traversers.traverser_shortest_path(hg, source="1", target="4"))
print(traversers.traverser_kout(hg, source="1", max_depth=2))
print(traversers.traverser_kout(hg, source="1", max_depth=1))
print(traversers.traverser_kneighbor(hg, source="1", max_depth=1))
