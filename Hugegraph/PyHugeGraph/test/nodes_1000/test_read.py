from PyHugeGraph import PyHugeGraphClient
from read_data import read_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_1000")

print(read_data.read_data(hg, 10))