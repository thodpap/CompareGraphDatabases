'''

Simply reads all edges and vertices from given graph

'''


def read_edges(hg, NUMBER_OF_VERTICES):

    import time
    
    counter = 0

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000

    for i in range(1, NUMBER_OF_VERTICES+1):

        time_before_edge_1 = time.time()
        res = hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="OUT", label="relationship")
        assert res.status_code == 200, f"Could not read edge starting from vertex {i}." 
        edges = eval(res.response)
        time_after_edge_1 = time.time()

        max_edge = max(max_edge, (time_after_edge_1 - time_before_edge_1)/len(edges["edges"]))
        min_edge = min(min_edge, (time_after_edge_1 - time_before_edge_1)/len(edges["edges"]))
        mean_edge += time_after_edge_1 - time_before_edge_1

        counter += len(edges["edges"])

    return {
        "mean_edge": mean_edge/counter,
        "max_edge": max_edge,
        "min_edge": min_edge,
    }

def read_vertices(hg, NUMBER_OF_VERTICES):

    import time

    counter = NUMBER_OF_VERTICES

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    for i in range(1, NUMBER_OF_VERTICES+1):

        time_before_vertex_1 = time.time()
        res = hg.get_vertex_by_id(vertex_id=f"1:{i}")
        assert res.status_code == 200, f"Could not read vertex {i}." 
        time_after_vertex_1 = time.time()
        max_vertex = max(max_vertex, time_after_vertex_1 - time_before_vertex_1)
        min_vertex = min(min_vertex, time_after_vertex_1 - time_before_vertex_1)
        mean_vertex += time_after_vertex_1 - time_before_vertex_1

    return {
        "mean_vertex": mean_vertex/counter,
        "max_vertex": max_vertex,
        "min_vertex": min_vertex,
    }

def read_data(hg, NUMBER_OF_VERTICES):

    edges = read_edges(hg, NUMBER_OF_VERTICES)
    vertices = read_vertices(hg, NUMBER_OF_VERTICES)

    return {
        "edges":edges,
        "vertices":vertices
    }