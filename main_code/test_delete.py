from PyHugeGraph import PyHugeGraphClient
from helper.delete_data import delete_data

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')
    # parser.add_argument('method', type=int, help='method: all together - 1 or one by one - 2')

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

    # if args.method == 1:
    #     allTogether = True
    # else:
    #     allTogether = False

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    # print(delete_data.delete_data(hg, 10))

    print(delete_data.delete_gremlin_alltogether(args.graph_name, vertices))

    # print(delete_data.delete_all_one_by_one_gremlin(args.graph_name, vertices))
    