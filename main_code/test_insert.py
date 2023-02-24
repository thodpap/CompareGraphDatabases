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

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)

    file = open(args.graph_name + ".txt", 'r')
    lines = file.readlines()
    # print(insert_data.insert_data(lines, hg))
    print(insert_data.insert_data_gremlin(graph_name=args.graph_name, lines=lines, NUMBER_OF_VERTICES=10))
    file.close()