from PyHugeGraph import PyHugeGraphClient
from delete_data import delete_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_100")

print(delete_data.delete_data(hg, 10))