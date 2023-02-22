from PyHugeGraph import PyHugeGraphClient
from read_data import read_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_100")

print(read_data.read_data(hg, 10))