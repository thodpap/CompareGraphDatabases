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
        res_e_1 = hg.create_edge(edge_label="relationship", outv=f"1:{vertex_1}", inv=f"1:{vertex_2}", outv_label="person", inv_label="person", properties={"strong":strong, "FromTo": f"{vertex_1} -> {vertex_2}"})
        assert res_e_1.status_code == 201, f"{vertex_1} -> {vertex_2} edge could not be created with error {res_e_1.response}"
        time_after_edge_1 = time.time()
        time_before_edge_2 = time.time()
        res_e_2 = hg.create_edge(edge_label="relationship", outv=f"1:{vertex_2}", inv=f"1:{vertex_1}", outv_label="person", inv_label="person", properties={"strong":strong, "FromTo": f"{vertex_2} -> {vertex_1}"})
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
            "mean": mean_vertex/counter_vertices,
            "max": max_vertex,
            "min": min_vertex,
            "number_of_vertices": counter_vertices
        },
        "edges":{    
            "mean": mean_edge/counter_edges,
            "max": max_edge,
            "min": min_edge,
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

    for line in lines[2:]:

        line = line.replace("\n","")
        vertex_1, vertex_2 = line.split(" ")

        task_1, task_2 = insert_edge_gremlin(graph_name=graph_name, outv=vertex_1, inv=vertex_2)
   
    while check_task_status(graph_name=graph_name, task_id=task_1) != "success":
        pass
   
    while check_task_status(graph_name=graph_name, task_id=task_2) != "success":
        pass

    return time.time() - initial_time

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# batch insertions

def batch_insert_vertices(hg, NUMBER_OF_VERTICES, batch=None, percentage=None):

    import random
    import time
    from tqdm import tqdm

    if percentage != None and batch == None:
        batch = NUMBER_OF_VERTICES*percentage

    if batch == None:
        batch == 100

    min_vertex = 100000000000
    max_vertex = 0
    mean_vertex = 0

    for i in tqdm(range(1, NUMBER_OF_VERTICES+1, batch), desc = 'tqdm() Progress Bar'):
        batched_list = []
        for j in range(i, min(i+batch, NUMBER_OF_VERTICES+1)):
            data_ = {
                "label":"person",
                 "properties": {
                    "name": str(j),
                    "age": random.randint(1, 100)
                }
            }
            batched_list.append(data_)
        time_before_batch = time.time()
        hg.create_multi_vertex(data=batched_list)
        time_after_batch = time.time()
        
        b = min(NUMBER_OF_VERTICES + 1 - i, batch)
        diff = (time_after_batch - time_before_batch)/b
        max_vertex = max(max_vertex, diff)
        min_vertex = min(min_vertex, diff)
        mean_vertex += time_after_batch - time_before_batch

    return {
            "max":max_vertex,
            "min":min_vertex,
            "mean":mean_vertex/NUMBER_OF_VERTICES
        }

def batch_inset_edges(hg, lines, NUMBER_OF_VERTICES, batch=None, percentage=None):

    import random
    import time
    from tqdm import tqdm

    if percentage != None and batch == None:
        batch = NUMBER_OF_VERTICES*percentage

    if batch == None:
        batch == 100   

    length = len(lines)
    print("length =", length)
    min_edge = 1e10
    max_edge = 0
    mean_edge = 0
    
    for i in tqdm(range(2, len(lines), batch), desc = 'tqdm() Progress Bar'):
        batched_list = []
        for j in range(i, min(i+ batch, length)):
            line = lines[j]
            line = line.replace("\n","")
            vertex_1, vertex_2 = line.split(" ")    
            data_ = {
                "label": "relationship",
                "outV": f"1:{vertex_1}",
                "inV": f"1:{vertex_2}",
                "outVLabel": "person",
                "inVLabel": "person",
                "properties": {
                    "strong": random.randint(1, 10),
                    "FromTo": f"{vertex_1} -> {vertex_2}"
                }
            }
            batched_list.append(data_)
            data_ = {
                "label": "relationship",
                "outV": f"1:{vertex_2}",
                "inV": f"1:{vertex_1}",
                "outVLabel": "person",
                "inVLabel": "person",
                "properties": {
                    "strong": random.randint(1, 10),
                    "FromTo": f"{vertex_2} -> {vertex_1}"
                }
            }
            batched_list.append(data_)
        
        time_before_edge_1 = time.time()
        hg.create_multi_edge(batched_list)
        time_after_edge_1 = time.time()

        b = min(length - i, batch)
        diff = (time_after_edge_1 - time_before_edge_1)/b
        max_edge = max(max_edge, diff)
        min_edge = min(min_edge, diff)
        mean_edge += time_after_edge_1 - time_before_edge_1
    

    return {
        "max":max_edge,
        "min":min_edge,
        "mean":mean_edge/(length - 2)
    } 

def batch_insert(hg, lines, NUMBER_OF_VERTICES, batch_vertices=None, batch_edges=None, percentage=None):

    vertices = batch_insert_vertices(hg=hg, NUMBER_OF_VERTICES=NUMBER_OF_VERTICES, batch=batch_vertices, percentage=percentage)
    edges = batch_inset_edges(hg=hg, lines=lines, NUMBER_OF_VERTICES=NUMBER_OF_VERTICES, batch=batch_edges, percentage=percentage)

    return {
        "vertices":vertices,
        "edges":edges
    }
    