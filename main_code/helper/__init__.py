def get_vertices_number(args):
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
    
    return vertices