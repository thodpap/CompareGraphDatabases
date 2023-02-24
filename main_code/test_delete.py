from PyHugeGraph import PyHugeGraphClient
from helper.delete_data import delete_data

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

    print(delete_data.delete_data(hg, 10))