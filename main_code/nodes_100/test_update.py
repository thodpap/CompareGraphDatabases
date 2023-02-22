from PyHugeGraph import PyHugeGraphClient
from update_data import update_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_100")

print(update_data.update_data(hg, 10))