from PyHugeGraph import PyHugeGraphClient
from helper.delete_data import delete_data
from helper import get_vertices_number

if __name__ == "__main__":
    import argparse
    
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Process names.')

    # Add an argument
    parser.add_argument('graph_name', type=str, help='the graph name')
    parser.add_argument('method', type=int, help='method: 0 means basic delete, all together - 1 or one by one - 2')

    # Parse the command-line arguments
    args = parser.parse_args()

    vertices = get_vertices_number(args)    
    
    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", args.graph_name)
    
    if args.method == 0:
        # print("Basic delete", hg.delete_vertex_by_id(vertex_id="1:23").response)
        print("Basic delete", delete_data.delete_data(hg, NUMBER_OF_vertices=100, direction="BOTH"))
        # print("Basic delete", delete_data.delete_edges(hg, NUMBER_OF_VERTICES=30, direction="BOTH"))
        # print("Basic delete", delete_data.delete_vertices(hg, NUMBER_OF_VERTICES=30))
    elif args.method == 1:
        print("Gremlin delete all together", delete_data.delete_gremlin_alltogether(args.graph_name, vertices))
    elif args.method == 2:
        print("Gremlin delete one by one", delete_data.delete_all_one_by_one_gremlin(args.graph_name, vertices))
    else:
        raise TypeError("Wrong method")