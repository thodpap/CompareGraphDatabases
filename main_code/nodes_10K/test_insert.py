from PyHugeGraph import PyHugeGraphClient
from insert_data import insert_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_10000")

file = open("10_nodes.txt", 'r')
lines = file.readlines()
print(insert_data.insert_data(lines, hg))
file.close()