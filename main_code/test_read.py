from PyHugeGraph import PyHugeGraphClient
from helper.read_data import read_data

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')

    # Parse the command-line arguments
    args = parser.parse_args()

    assert "node_1" in args.graph_name


    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    if args.graph_name == "node_10":
        vertexes = 10
    elif args.graph_name == "node_100":
        vertexes = 100
    elif args.graph_name == "node_1000":
        vertexes = 1000
    elif args.graph_name == "node_10000":
        vertexes = 10000
    elif args.graph_name == "node_100000":
        vertexes = 100000
    elif args.graph_name == "node_1000000":
        vertexes = 1000000
    else:
        assert False

    # print(read_data.read_data(hg, 10))

    # print(read_data.read_vertex_gremlin("node_10", 1, False))

    print("Sync read vertexes", read_data.read_vertexes_gremlin(args.graph_name, vertexes, True))
    print("Async read vertexes", read_data.read_vertexes_gremlin(args.graph_name, vertexes, False))
    print()
    print("Sync read edges", read_data.read_edges_gremlin(args.graph_name, vertexes, True))
    print("Async read edges", read_data.read_edges_gremlin(args.graph_name, vertexes, False))