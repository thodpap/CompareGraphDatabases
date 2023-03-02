from PyHugeGraph import PyHugeGraphClient
from helper.update_data import update_data
from helper import get_vertices_number

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')
    parser.add_argument('method', type=int, help='method: 0: basic update, 1: gremlin update, 2: both, 3: batch update')

    # Parse the command-line arguments
    args = parser.parse_args()

    vertices = get_vertices_number(args)    
    
    print(args.graph_name + ".txt")
    file = open(args.graph_name + ".txt", 'r')
    
    lines = file.readlines()

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)
    
    if args.method == 0:
        print("basic update", update_data.update_data(hg, vertices))
    elif args.method == 1:
        print("Gremlin update", update_data.update_gremlin(args.graph_name, vertices))
    elif args.method == 2:
        print("basic update", update_data.update_data(hg, vertices))
        print("Gremlin update", update_data.update_gremlin(args.graph_name, vertices))
    elif args.method == 3:
        print("basic update", update_data.batch_update(hg=hg, lines=lines[2:100002], NUMBER_OF_VERTICES=10000, batch_vertices=200, batch_edges=50, percentage=None))
    else:
        raise TypeError("Wrong method")



