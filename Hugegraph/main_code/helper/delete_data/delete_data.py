'''

deletes all the edges and vertices from the graph. 

'''


def delete_edges(hg, NUMBER_OF_VERTICES, direction="OUT"):

    import time
    
    counter = 0

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000
    # print(direction)
    initial_time = time.time()
    for i in range(1, NUMBER_OF_VERTICES+1):

        
        edges = eval(hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="OUT", label="relationship").response)
        # if i == 23:
        #     print(len(edges["edges"]), direction)
        #     print(edges["edges"])
        data_ = edges["edges"]
        counter += len(data_)
   
        for edge in data_:
                        
            id = edge['id']
            time_before_edge_1 = time.time()
            res = hg.delete_edge_by_id(id)
            assert res.status_code == 204, "Could not delete edge " + id + f" with error {res.response}."
            time_after_edge_1 = time.time()
            max_edge = max(max_edge, time_after_edge_1 - time_before_edge_1)
            min_edge = min(min_edge, time_after_edge_1 - time_before_edge_1)
            mean_edge += time_after_edge_1 - time_before_edge_1

        if direction == "BOTH":
            edges = eval(hg.get_edge_by_condition(vertex_id=f"\"1:{i}\"", direction="IN", label="relationship").response)
            # if i == 23:
            #     print(len(edges["edges"]), direction)
            #     print(edges["edges"])
            data_ = edges["edges"]
            counter += len(data_)
    
            for edge in data_:
                            
                id = edge['id']
                time_before_edge_1 = time.time()
                res = hg.delete_edge_by_id(id)
                assert res.status_code == 204, "Could not delete edge " + id + f" with error {res.response}."
                time_after_edge_1 = time.time()
                max_edge = max(max_edge, time_after_edge_1 - time_before_edge_1)
                min_edge = min(min_edge, time_after_edge_1 - time_before_edge_1)
                mean_edge += time_after_edge_1 - time_before_edge_1


       

    return {
        "mean": mean_edge/counter,
        "max": max_edge,
        "min": min_edge,
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

        try:
            time_before_vertex_1 = time.time()
            res = hg.delete_vertex_by_id(vertex_id=f"1:{i}")
            assert res.status_code == 204, f"Could not delete vertex {i} with error {res.response}." 
            time_after_vertex_1 = time.time()
            max_vertex = max(max_vertex, time_after_vertex_1 - time_before_vertex_1)
            min_vertex = min(min_vertex, time_after_vertex_1 - time_before_vertex_1)
            mean_vertex += time_after_vertex_1 - time_before_vertex_1
        except Exception as e:
            continue

    return {
        "mean": mean_vertex/counter,
        "max": max_vertex,
        "min": min_vertex,
        "total_time": time.time() - initial_time
    }


def delete_data(hg, NUMBER_OF_vertices, direction="OUT"):

    edges = delete_edges(hg, NUMBER_OF_VERTICES=NUMBER_OF_vertices, direction=direction)
    vertices = delete_vertices(hg, NUMBER_OF_vertices)
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

def count_edges(graph_name="node_10"):
    import requests

    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().E().count()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)["result"]["data"][0]

# def delete_edges_vertex_gremlin_sync(graph_name="node_10", vertex=1):
#     import requests
#     url_ = f"http://localhost:8081/gremlin"
#     query_ = graph_name + f'.traversal().V("1:{vertex}")'

#     response = requests.delete(url_ + "?gremlin=" + query_)
    
#     return eval(response.content)["result"]["data"]


#########################################################
# Drop edges and vertices

def delete_all_edges_gremlin_sync(graph_name="node_10"):
    import requests

    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().E().drop()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)

def delete_all_vertices_gremlin_sync(graph_name="node_10"):
    import requests

    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().V().drop()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)

def delete_edges_gremlin_alltogether(graph_name="node_10"):
    import time

    edges_count = count_edges()

    start_time = time.time()
    
    delete_all_edges_gremlin_sync(graph_name)
    
    total = time.time() - start_time

    if edges_count == 0:
        edges_count += 1
        
    return {
        "min": 0,
        "mean": total / edges_count, 
        "total_time": total,
        "max": 0,
    }

def delete_vertices_gremlin_alltogether(graph_name="node_10", Nodes=10):
    import time

    start_time = time.time()
    print(delete_all_vertices_gremlin_sync(graph_name))
    total = time.time() - start_time

    return {
        "min": 0,
        "mean": total / Nodes, 
        "total_time": total,
        "max": 0,
    }

def delete_gremlin_alltogether(graph_name="node_10", Nodes=10):
    return {
        "edges": delete_edges_gremlin_alltogether(graph_name),
        "vertices": delete_vertices_gremlin_alltogether(graph_name, Nodes)
    }


# -------------------------------------------------------------------------------------


def read_edges_of_vertex_gremlin(graph_name="node_10", vertex=1):
    import requests
    
    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().V("1:{vertex}").outE().count()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)["result"]["data"][0]

def delete_edges_by_vertex_gremlin(graph_name="node_10", vertex=1):
    import requests
    
    nodes_count = read_edges_of_vertex_gremlin(graph_name, vertex)
    
    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().V("1:{vertex}").outE().drop()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content), nodes_count

def delete_vertices_by_vertex_gremlin(graph_name="node_10", vertex=1):
    import requests
    
    url_ = f"http://localhost:8081/gremlin"
    query_ = graph_name + f'.traversal().V("1:{vertex}").drop()'

    response = requests.get(url_ + "?gremlin=" + query_)
    return eval(response.content)

def delete_edges_gremlin_one_by_one(graph_name="node_10", Nodes=10):
    import time

    min_ = 1e1000
    max_ = 0
    mean_ = 0

    start_time = time.time()
    
    for vertex in range(1, Nodes + 1):
        begin = time.time()
        
        response, edge_count = delete_edges_by_vertex_gremlin(graph_name, vertex)
        # print(response)
        end = time.time() - begin

        min_ = min(min_, end / edge_count)
        max_ = max(max_, end / edge_count)
        mean_ += end / edge_count

    total = time.time() - start_time

    return {
        "min": min_,
        "mean": mean_, 
        "max": max_, 
        "total_time": total
    }    


def delete_vertices_gremlin_one_by_one(graph_name="node_10", Nodes=10):
    import time

    min_ = 1e1000
    max_ = 0
    mean_ = 0

    start_time = time.time()
    
    for vertex in range(1, Nodes + 1):
        begin = time.time()
        
        response = delete_vertices_by_vertex_gremlin(graph_name, vertex)
        
        end = time.time() - begin

        min_ = min(min_, end)
        max_ = max(max_, end)
        mean_ += end

    total = time.time() - start_time

    return {
        "min": min_,
        "mean": mean_ / Nodes, 
        "max": max_, 
        "total_time": total
    }    

def delete_all_one_by_one_gremlin(graph_name, vertices):
    return {
        "edges": delete_edges_gremlin_one_by_one(graph_name, vertices), 
        "vertices": delete_vertices_gremlin_one_by_one(graph_name, vertices)
    }