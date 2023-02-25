from PyHugeGraph import PyHugeGraphClient
from helper.insert_data import insert_data
from helper import get_vertices_number

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')
    parser.add_argument('method', type=int, help='method: 0: basic insert, 1: insert with gremlin, 2: both')

    # Parse the command-line arguments
    args = parser.parse_args()

    vertices = get_vertices_number(args)

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    file = open(args.graph_name + ".txt", 'r')
    lines = file.readlines()

    if args.method == 0:
        print("basic insert", insert_data.insert_data(lines, hg))
    elif args.method == 1:
        print("gremlin insert", insert_data.insert_data_gremlin(graph_name=args.graph_name, lines=lines, NUMBER_OF_VERTICES=vertices))
    elif args.method == 2:
        print("basic insert", insert_data.insert_data(lines, hg))
        print("gremlin insert", insert_data.insert_data_gremlin(graph_name=args.graph_name, lines=lines, NUMBER_OF_VERTICES=vertices))
    else:
        file.close()
        raise TypeError("Wrong method")
    
    file.close()