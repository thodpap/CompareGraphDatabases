from PyHugeGraph import PyHugeGraphClient
from read_data import read_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_10")

print(read_data.read_data(hg, 10))