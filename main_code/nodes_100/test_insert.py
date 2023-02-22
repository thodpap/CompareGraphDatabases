from PyHugeGraph import PyHugeGraphClient
from insert_data import insert_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_100")

file = open("100_nodes.txt", 'r')
lines = file.readlines()
print(insert_data.insert_data(lines, hg))
file.close()