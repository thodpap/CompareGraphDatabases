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

if __name__ == "__main__":

    import sys
    sys.path.insert(1, 'nodes_10/PyHugeGraph')

    from PyHugeGraph import PyHugeGraphClient

    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "nodes_10")
    print(hg.clear_graph_alldata().status_code)

    file = open("../10_nodes.txt", 'r')
    lines = file.readlines()
    insert_data(lines, hg)
    file.close()
    