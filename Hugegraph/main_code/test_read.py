from PyHugeGraph import PyHugeGraphClient
from helper.read_data import read_data
from helper import get_vertices_number

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')
    parser.add_argument('method', type=int, help='method: 0: normal read_data, 1: sync, 2: async, 3: run all')

    # Parse the command-line arguments
    args = parser.parse_args()

    assert "node_1" in args.graph_name


    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    vertexes = get_vertices_number(args)

    if args.method == 0:
        print("Normal: ", read_data.read_data(hg, vertexes))
    elif args.method == 1:
        print("Sync: ", read_data.read_gremlin(args.graph_name, vertexes, True))
    elif args.method == 2:
        print("Async: ", read_data.read_gremlin(args.graph_name, vertexes, False))
    elif args.method == 3:
        print("Normal: ", read_data.read_data(hg, vertexes))
        print("Sync: ", read_data.read_gremlin(args.graph_name, vertexes, True))
        print("Async: ", read_data.read_gremlin(args.graph_name, vertexes, False))
    else:
        raise TypeError("Wrong method")