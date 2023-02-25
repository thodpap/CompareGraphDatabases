from PyHugeGraph import PyHugeGraphClient
from helper.insert_data import insert_data



if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')

    # Parse the command-line arguments
    args = parser.parse_args()

    assert "node_1" in args.graph_name

    if args.graph_name == "node_10":
        vertices = 10
    elif args.graph_name == "node_100":
        vertices = 100
    elif args.graph_name == "node_1000":
        vertices = 1000
    elif args.graph_name == "node_10000":
        vertices = 10000
    elif args.graph_name == "node_100000":
        vertices = 100000
    elif args.graph_name == "node_1000000":
        vertices = 1000000
    else:
        assert False

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    file = open(args.graph_name + ".txt", 'r')
    lines = file.readlines()
    # print(insert_data.insert_data(lines, hg))
    print(insert_data.insert_data_gremlin(graph_name=args.graph_name, lines=lines, NUMBER_OF_VERTICES=vertices))
    file.close()