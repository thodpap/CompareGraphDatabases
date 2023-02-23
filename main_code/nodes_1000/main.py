from PyHugeGraph import PyHugeGraphClient
from insert_data import insert_data
from delete_data import delete_data
from update_data import update_data
from traversers import traversers
from read_data import read_data

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_1000")

