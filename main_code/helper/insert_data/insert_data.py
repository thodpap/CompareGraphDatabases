'''

Takes the lines of a file (file = open(".txt", 'r'), lines = f.readlines()) and a hugegraph drive as arguments and inserts the data to the GraphDB 

'''

def insert_data(lines, hg):

    import time
    import random

    myset = set()
    counter_vertices = 0
    counter_edges = 0

    mean_vertex = 0
    max_vertex = 0
    min_vertex = 1000000000000

    mean_edge = 0
    max_edge = 0
    min_edge = 1000000000000

    initial_time = time.time()
    for line in lines[2:]:
        
        line = line.replace("\n","")
        vertex_1, vertex_2 = line.split(" ")

        vertex_1_data =  {
            "label": "person",
            "properties": {
                "name": vertex_1,
                "age": random.randint(1, 100)
            }
        }

        vertex_2_data =  {
            "label": "person",
            "properties": {
                "name": vertex_2,
                "age": random.randint(1, 100)
            }
        }

        if vertex_1 not in myset:
            time_before_vertex_1 = time.time()
            res_1 = hg.create_vertex(data=vertex_1_data)
            res_1_code = res_1.status_code
            res_1 = eval(res_1.response)
            assert res_1_code == 201, f"{vertex_1} could not be inserted with error {res_1}"
            time_after_vertex_1 = time.time()
            time_vertex_1 = time_after_vertex_1 - time_before_vertex_1
            max_vertex = max(max_vertex, time_vertex_1)
            min_vertex = min(min_vertex, time_vertex_1)
            mean_vertex += time_vertex_1
            myset.add(vertex_1)
            counter_vertices += 1

        if vertex_2 not in myset:
            time_before_vertex_2 = time.time()
            res_2 = hg.create_vertex(data=vertex_2_data)
            res_2_code = res_2.status_code
            res_2 = eval(res_2.response)
            assert res_2_code == 201, f"{vertex_2} could not be inserted with error {res_2}"
            time_after_vertex_2 = time.time()
            time_vertex_2 = time_after_vertex_2 - time_before_vertex_2
            max_vertex = max(max_vertex, time_vertex_2)
            min_vertex = min(min_vertex, time_vertex_2)
            mean_vertex += time_vertex_2
            myset.add(vertex_2)
            counter_vertices += 1
        
        
        strong = random.randint(1, 10)

        time_before_edge_1 = time.time()
        res_e_1 = hg.create_edge(edge_label="relationship", outv=res_1["id"], inv=res_2["id"], outv_label="person", inv_label="person", properties={"strong":strong, "FromTo": f"{vertex_1} -> {vertex_2}"})
        assert res_e_1.status_code == 201, f"{vertex_1} -> {vertex_2} edge could not be created with error {res_e_1.response}"
        time_after_edge_1 = time.time()
        time_before_edge_2 = time.time()
        res_e_2 = hg.create_edge(edge_label="relationship", outv=res_2["id"], inv=res_1["id"], outv_label="person", inv_label="person", properties={"strong":strong, "FromTo": f"{vertex_2} -> {vertex_1}"})
        assert res_e_2.status_code == 201, f"{vertex_2} -> {vertex_1} edge could not be created with error {res_e_2.response}"       
        time_after_edge_2 = time.time()

        time_edge_1 = time_after_edge_1 - time_before_edge_1
        time_edge_2 = time_after_edge_2 - time_before_edge_2
        max_edge = max(max_edge, time_edge_1, time_edge_2)
        min_edge = min(min_edge, time_edge_1, time_edge_2)        

        mean_edge += time_edge_1 + time_edge_2

        counter_edges += 2

    return {
        "vertices":{
            "mean_vertex": mean_vertex/counter_vertices,
            "max_vertex": max_vertex,
            "min_vertex": min_vertex,
            "number_of_vertices": counter_vertices
        },
        "edges":{    
            "mean_edge": mean_edge/counter_edges,
            "max_edge": max_edge,
            "min_edge": min_edge,
            "number_of_edges": counter_edges
        },
        "total_time": time.time() - initial_time
    }


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


def insert_vertex_gremlin(graph_name, name, age, label="person"):

    import requests

    query_ = graph_name + f'.traversal().addV("{label}").property("name", "{name}").property("age", {age})'
    url_ = f"http://localhost:8081/graphs/{graph_name}/jobs/gremlin"
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


def insert_edge_gremlin(graph_name, outv, inv):

    import random
    import requests

    strong = random.randint(1, 10)

    query_out_in = graph_name + f'.traversal().V("1:{outv}").as("{outv}").V("1:{inv}").as("{inv}").addE("relationship").from("{outv}").to("{inv}").property("strong", {strong}).property("FromTo", "{outv} -> {inv}")'
    query_in_out = graph_name + f'.traversal().V("1:{inv}").as("{inv}").V("1:{outv}").as("{outv}").addE("relationship").from("{inv}").to("{outv}").property("strong", {strong}).property("FromTo", "{inv} -> {outv}")'

    url_ = f"http://localhost:8081/graphs/{graph_name}/jobs/gremlin"
    headers_ = {"Content-Type": "application/json", "Accept": "application/json"}

    json_out_in = {
        "gremlin": query_out_in,
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {}
    }

    json_in_out = {
        "gremlin": query_in_out,
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {}
    }

    response_out_in = requests.post(
        url=url_,
        headers=headers_,
        json=json_out_in
    )

    response_in_out = requests.post(
        url=url_,
        headers=headers_,
        json=json_in_out
    )

    return [eval(response_out_in.content)["task_id"], eval(response_in_out.content)["task_id"]]

def check_task_status(graph_name, task_id):
    
    import requests

    url = f"http://localhost:8081/graphs/{graph_name}/tasks/{task_id}"
    response = requests.get(url=url)
    return eval(response.content)["task_status"]

def insert_data_gremlin(lines, graph_name, NUMBER_OF_VERTICES):

    import time
    import random

    vertices_set_tasks = set()
    edges_set_tasks = set()

    initial_time = time.time()
    for vertex in range(1, NUMBER_OF_VERTICES+1):
        # vertices_set_tasks.add(insert_vertex_gremlin(graph_name=graph_name, name=vertex, age=random.randint(1, 100)))
        insert_vertex_gremlin(graph_name=graph_name, name=vertex, age=random.randint(1, 100))

    # init = len(vertices_set_tasks)
    # temp = []
    # while init > 0:

    #     for task in vertices_set_tasks:
    #         if check_task_status(graph_name=graph_name, task_id=task):
    #             init -= 1
    #             temp.append(task)

    #     for task in temp:
    #         vertices_set_tasks.remove(task)

    #     temp = []

    for line in lines[2:]:

        line = line.replace("\n","")
        vertex_1, vertex_2 = line.split(" ")

        task_1, task_2 = insert_edge_gremlin(graph_name=graph_name, outv=vertex_1, inv=vertex_2)
        # edges_set_tasks.add(task_1)
        # edges_set_tasks.add(task_2)

    # init = len(edges_set_tasks)
    # temp = []
    # while init > 0:

    #     for task in edges_set_tasks:
    #         if check_task_status(graph_name=graph_name, task_id=task):
    #             init -= 1
    #             temp.append(task)

    #     for task in temp:
    #         edges_set_tasks.remove(task)

    #     temp = []

    return time.time() - initial_time

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# batch insertions

def batch_insert(hg, lines, NUMBER_OF_VERTICES, batch=None, percentage=None):

    if percentage != None and batch == None:
        batch = NUMBER_OF_VERTICES*percentage

    if batch == None:
        batch == 100

    batched_list = []
    for i in range(1, NUMBER_OF_VERTICES+1):
        for j in range(100):
        
