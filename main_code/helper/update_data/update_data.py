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

    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        edges = eval(hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="OUT", label="relationship").response)
        
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
        "total_time": time.time() - initial_time
    }


def update_vertices(hg, NUMBER_OF_VERTICES):

    import time
    import random

    counter = NUMBER_OF_VERTICES

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        rand_1 = random.randint(1, 100)
        time_before_vertex_1 = time.time()
        res = hg.update_vertex_properties(vertex_id=f"\"1:{i}\"", label="person", properties={"age":rand_1})
        assert res.status_code == 200, f"Could not update vertex {i}." 
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


def update_data(hg, NUMBER_OF_VERTICES):

    edges = update_edges(hg, NUMBER_OF_VERTICES)
    vertices = update_vertices(hg, NUMBER_OF_VERTICES)

    return {
        "edges":edges,
        "vertices":vertices
    }

# ----------------------------------------------------------------------------------
# Gremlin area

def update_vertice_age_gremlin(graph_name="node_10", vertex=1, age=50):
    import requests

    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f""".traversal().V("1:{vertex}").property('age', {age})"""

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)["result"]["data"]

def update_vertices_gremlin(graph_name, vertices):
    import time
    import random

    mean_ = 0
    min_ = 1e10
    max_ = 0

    start = time.time()
    for vertex in range(1, vertices + 1):
        age = random.randint(1,100)
        
        begin_time = time.time()
        update_vertice_age_gremlin(graph_name, vertex, age)
        ti = time.time() - begin_time

        min_ = min(min_, ti)
        max_ = max(max_, ti)
        mean_ += ti

    return {
        "min": min_,
        "max": max_,
        "mean": mean_ / vertices,
        "total_time": time.time() - start
    }

