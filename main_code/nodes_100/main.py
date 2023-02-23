from PyHugeGraph import PyHugeGraphClient
from insert_data import insert_data
from delete_data import delete_data
from update_data import update_data
from traversers import traversers
from read_data import read_data
import matplotlib.pyplot as plt
import numpy as np

def mapping(l, key_1, key_2):
    return list(map(lambda x: x[key_1][key_2], l))

NUMBER_OF_VERTICES_ = 10

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_100")

file = open("10_nodes.txt", 'r')
lines = file.readlines()
time = []
time.append(insert_data.insert_data(lines, hg))
time.append(update_data.update_data(hg, NUMBER_OF_VERTICES_))
time.append(read_data.read_data(hg=hg, NUMBER_OF_VERTICES=NUMBER_OF_VERTICES_))
time.append(delete_data.delete_data(hg=hg, NUMBER_OF_vertices=NUMBER_OF_VERTICES_))

print("time_insert:", time[0])
print("time_update:", time[1])
print("time_read:", time[2])
print("time_delete:", time[3])

x_labels = ["insert", "update", "read", "delete"]
X_axis = np.arange(len(x_labels))*2

plt.figure()
plt.xticks(X_axis, x_labels) #, rotation=45
plt.title("Vertices")

plt.bar(X_axis - 0.4, mapping(time, "vertices", "min_vertex"), 0.4, label="min")
plt.bar(X_axis, mapping(time, "vertices", "mean_vertex"), 0.4, label="mean")
plt.bar(X_axis + 0.4, mapping(time, "vertices", "max_vertex"), 0.4, label="max")
plt.legend()
plt.savefig("plots/vertices.png")

plt.figure()
plt.xticks(X_axis, x_labels, rotation=45)
plt.title("edges")

plt.bar(X_axis - 0.4, mapping(time, "edges", "min_edge"), 0.4, label="min")
plt.bar(X_axis, mapping(time, "edges", "mean_edge"), 0.4, label="mean")
plt.bar(X_axis + 0.4, mapping(time, "edges", "max_edge"), 0.4, label="max")
plt.legend()
plt.savefig("plots/edges.png")