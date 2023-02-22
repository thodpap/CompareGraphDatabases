'''

    update all the edges (strong attribute) and vertices (age attribute) from the graph. 

'''

def update_edges(hg, NUMBER_OF_VERTICES):

    import time
    import random
    
    counter = 0

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000

    for i in range(1, NUMBER_OF_VERTICES+1):

        edges = eval(hg.get_edge_by_condition(vertex_id=f"\"{i}\"", direction="OUT", label="relationship").response)
        
        data_ = edges["edges"]
        counter += len(data_)

        for edge in data_:
                        
            id = edge['id']
            rand_1 = random.randint(1, 10)
            time_before_edge_1 = time.time()
            res = hg.update_edge_properties(edge_id=id, properties={"strong":rand_1})
            assert res.status_code == 200, "Could not update " + id + " edge."
            time_after_edge_1 = time.time()

            max_edge = max(max_edge, time_after_edge_1 - time_before_edge_1)
            min_edge = min(min_edge, time_after_edge_1 - time_before_edge_1)
            mean_edge += time_after_edge_1 - time_before_edge_1

    return {
        "mean_edge": mean_edge/counter,
        "max_edge": max_edge,
        "min_edge": min_edge,
    }


def update_vertices(hg, NUMBER_OF_VERTICES):

    import time
    import random

    counter = NUMBER_OF_VERTICES

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    for i in range(1, NUMBER_OF_VERTICES+1):

        rand_1 = random.randint(1, 100)
        time_before_vertex_1 = time.time()
        res = hg.update_vertex_properties(vertex_id=f"\"{i}\"", label="person", properties={"age":rand_1})
        assert res.status_code == 200, f"Could not update vertex {i}." 
        time_after_vertex_1 = time.time()
        max_vertex = max(max_vertex, time_after_vertex_1 - time_before_vertex_1)
        min_vertex = min(min_vertex, time_after_vertex_1 - time_before_vertex_1)
        mean_vertex += time_after_vertex_1 - time_before_vertex_1

    return {
        "mean_vertex": mean_vertex/counter,
        "max_vertex": max_vertex,
        "min_vertex": min_vertex,
    }


def update_data(hg, NUMBER_OF_VERTICES):

    edges = update_edges(hg, NUMBER_OF_VERTICES)
    vertices = update_vertices(hg, NUMBER_OF_VERTICES)

    return {
        "edges":edges,
        "vertices":vertices
    }