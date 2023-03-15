from PyHugeGraph import PyHugeGraphClient
from helper.insert_data import insert_data
from helper.delete_data import delete_data
from helper.update_data import update_data
from helper.traversers import traversers
from helper.read_data import read_data
import matplotlib.pyplot as plt
import numpy as np

from helper import get_vertices_number

def mapping(l, key_1, key_2):
    return list(map(lambda x: x[key_1][key_2], l))


NUMBER_OF_VERTICES_ = 10

databases = ['node_10', 'node_100', 'node_1000'] #, 'node_10000', 'node_100000', 'node_1000000']

def plot(title, x_labels, X_axis, time, option="vertices"):
    plt.figure()
    plt.title(title)

    plt.xticks(X_axis, x_labels) #, rotation=45
    plt.bar(X_axis - 0.4, mapping(time, option, "min"), 0.4, label="min")
    plt.bar(X_axis, mapping(time, option, "mean"), 0.4, label="mean")
    plt.bar(X_axis + 0.4, mapping(time, option, "max"), 0.4, label="max")

    plt.legend()

def execute_database(database, large=True):
    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", database)
    
    vertices = get_vertices_number(database, False)

    file = open(database + ".txt", 'r')
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

    plot("Basic sequence on " + database + ": Vertices", x_labels, X_axis, time, "vertices")
    plot("Basic sequence on " + database + ": Edges", x_labels, X_axis, time, "edges")

    # if not large:
    #     # Compare different inserts
    #     time = [time[0]]
    #     # time.append(insert_data.insert_data_gremlin(graph_name=database, lines=lines, NUMBER_OF_VERTICES=vertices))
    #     time.append(insert_data.batch_insert(hg=hg, lines=lines, NUMBER_OF_VERTICES=vertices, batch_vertices=500, batch_edges=250))
        
    #     x_labels = ["normal", "batch"]
    #     X_axis = np.arange(len(x_labels))*2
    #     plot("Inserts on " + database + ": Vertices", x_labels, X_axis, time, "vertices")
    #     plot("Inserts on " + database + ": Edges", x_labels, X_axis, time, "edges")

    plt.show()
    return time

results = {}
for db in databases:
    results[db] = execute_database(db, False)