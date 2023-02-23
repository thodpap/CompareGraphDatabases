'''

deletes all the edges and vertices from the graph. 

'''


def delete_edges(hg, NUMBER_OF_VERTICES):

    import time
    
    counter = 0

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000
    
    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        
        edges = eval(hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="OUT", label="relationship").response)

        data_ = edges["edges"]
        counter += len(data_)
   
        for edge in data_:
                        
            id = edge['id']
            time_before_edge_1 = time.time()
            res = hg.delete_edge_by_id(id)
            assert res.status_code == 204, "Could not delete edge " + id + "."
            time_after_edge_1 = time.time()
            max_edge = max(max_edge, time_after_edge_1 - time_before_edge_1)
            min_edge = min(min_edge, time_after_edge_1 - time_before_edge_1)
            mean_edge += time_after_edge_1 - time_before_edge_1
       

    return {
        "mean_edge": mean_edge/counter,
        "max_edge": max_edge,
        "min_edge": min_edge,
        "total_time": time.time() - initial_time
    }



def delete_vertices(hg, NUMBER_OF_VERTICES):

    import time
    
    counter = NUMBER_OF_VERTICES

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        time_before_vertex_1 = time.time()
        res = hg.delete_vertex_by_id(vertex_id=f"1:{i}")
        assert res.status_code == 204, f"Could not delete vertex {i}." 
        time_after_vertex_1 = time.time()
        max_vertex = max(max_vertex, time_after_vertex_1 - time_before_vertex_1)
        min_vertex = min(min_vertex, time_after_vertex_1 - time_before_vertex_1)
        mean_vertex += time_after_vertex_1 - time_before_vertex_1

    return {
        "mean_vertex": mean_vertex/counter,
        "max_vertex": max_vertex,
        "min_vertex": min_vertex,
        "total_time": time.time() - initial_time
    }


def delete_data(hg, NUMBER_OF_vertices):

    edges = delete_edges(hg, NUMBER_OF_vertices)
    vertices = delete_vertices(hg, NUMBER_OF_vertices)
    return {
        "edges":edges,
        "vertices":vertices
    }
       