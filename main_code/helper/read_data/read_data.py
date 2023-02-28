'''

Simply reads all edges and vertices from given graph

'''


def read_edges(hg, NUMBER_OF_VERTICES):

    import time
    
    counter = 0

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000
    counter_edges = 0
    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        time_before_edge_1 = time.time()
        res = hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="OUT", label="relationship")
        assert res.status_code == 200, f"Could not read edge starting from vertex {i}." 
        edges = eval(res.response)
        time_after_edge_1 = time.time()
        
        max_edge = max(max_edge, (time_after_edge_1 - time_before_edge_1)/len(edges["edges"]))
        min_edge = min(min_edge, (time_after_edge_1 - time_before_edge_1)/len(edges["edges"]))
        
        mean_edge += time_after_edge_1 - time_before_edge_1
        
        counter_edges += len(edges["edges"])

    return {
        "mean": mean_edge/counter_edges,
        "max": max_edge,
        "min": min_edge,
        "total_time": time.time() - initial_time
    }

def read_vertices(hg, NUMBER_OF_VERTICES):

    import time

    counter = NUMBER_OF_VERTICES

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        time_before_vertex_1 = time.time()
        res = hg.get_vertex_by_id(vertex_id=f"1:{i}")
        assert res.status_code == 200, f"Could not read vertex {i}."
        # print(res.response) 
        time_after_vertex_1 = time.time()
        max_vertex = max(max_vertex, time_after_vertex_1 - time_before_vertex_1)
        min_vertex = min(min_vertex, time_after_vertex_1 - time_before_vertex_1)
        mean_vertex += time_after_vertex_1 - time_before_vertex_1

    return {
        "mean": mean_vertex/counter,
        "max": max_vertex,
        "min": min_vertex,
        "total_time": time.time() - initial_time
    }

def read_data(hg, NUMBER_OF_VERTICES):

    vertices = read_vertices(hg, NUMBER_OF_VERTICES)
    edges = read_edges(hg, NUMBER_OF_VERTICES)
    

    return {
        "edges":edges,
        "vertices":vertices
    }


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_task_status(graph_name, task_id):
    import requests

    url = f"http://localhost:8081/graphs/{graph_name}/tasks/{task_id}"
    response = requests.get(url=url)
    return eval(response.content)["task_status"]

def read_vertex_gremlin(graph_name, vertex=1, sync=True):
    import requests
    if sync:
        url_ = f"http://localhost:8081/gremlin"
        query_ = graph_name + f'.traversal().V("1:{vertex}")'

        response = requests.get(url_ + "?gremlin=" + query_)
        
        return eval(response.content)["result"]["data"]
    else:
        url_ = f"http://localhost:8081/graphs/{graph_name}/jobs/gremlin"
        query_ = graph_name + f'.traversal().V("1:{vertex}")'
        headers_ = {"Content-Type": "application/json", "Accept": "application/json"}

        json_ = {
            "gremlin": query_,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {}
        }

        response = requests.post(
            url=url_,
            headers=headers_,
            json=json_
        )
        return eval(response.content)["task_id"]


def read_vertexes_gremlin(graph_name, Nodes, sync=True):
    import requests
    import time

    start_time = time.time()

    min_ = 1e1000
    max_ = 0
    mean_ = 0

    for vertex in range(1, Nodes + 1):
        before_time = time.time()
        result = read_vertex_gremlin(graph_name, vertex, sync)
        
        if sync:
            ti = time.time() - before_time
            min_ = min(min_, ti)
            max_ = max(max_, ti)
            mean_ += ti

    if not sync:
        init = Nodes
        temp = []
        
        while check_task_status(graph_name=graph_name, task_id=result) != "success":
            pass
        total = time.time() - start_time

        return {
            "total_time": total
        }
    
    total = time.time() - start_time
    mean_ /= Nodes
    
    return {
        "min": min_,
        "mean": mean_, 
        "max": max_, 
        "total_time": total
    }

def read_edges_of_vertex_gremlin(graph_name="node_10", vertex=1, sync=True):
    import requests
    if sync:
        url_ = f"http://localhost:8081/gremlin"
        query_ = graph_name + f'.traversal().V("1:{vertex}").outE()'

        response = requests.get(url_ + "?gremlin=" + query_)
        return eval(response.content)["result"]["data"]
    else:
        url_ = f"http://localhost:8081/graphs/{graph_name}/jobs/gremlin"
        query_ = graph_name + f'.traversal().V("1:{vertex}").outE()'
        headers_ = {"Content-Type": "application/json", "Accept": "application/json"}

        json_ = {
            "gremlin": query_,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {}
        }

        response = requests.post(
            url=url_,
            headers=headers_,
            json=json_
        )
        return eval(response.content)["task_id"]

    
def read_edges_gremlin(graph_name="node_10", Nodes=10, sync=True):
    import requests
    import time

    start_time = time.time()

    min_ = 1e1000
    max_ = 0
    mean_ = 0
    total_size = 0
    counter = 0
    for vertex in range(1, Nodes + 1):
        before_time = time.time()
        result = read_edges_of_vertex_gremlin(graph_name, vertex, sync)
        
        if sync:
            ti = time.time() - before_time
        
            min_ = min(min_, ti / len(result))
            max_ = max(max_, ti / len(result))
            mean_ += ti 

            total_size += len(result)
    
    if not sync:
        init = Nodes
        temp = []
        
        while check_task_status(graph_name=graph_name, task_id=result) != "success":
            pass

        total = time.time() - start_time

        return {
            "total_time": total
        }
  
    total = time.time() - start_time
    
    return {
        "min": min_,
        "mean": mean_ / total_size, 
        "max": max_, 
        "total_time": total
    }

def read_gremlin(graph_name, vertices, sync=True):
    return {
        "vertices": read_vertexes_gremlin(graph_name, vertices, sync),
        "edges": read_edges_gremlin(graph_name, vertices, sync)
    }