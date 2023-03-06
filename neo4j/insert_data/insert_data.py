import random


def insert_vertex(person_name, driver):
    def  insert_vertex_(tx, person_name):
        age = random.randint(1,100)
        q1 = "CREATE (n:Person{name:$name , age:$age1})" 
        tx.run(q1, name = str(person_name), age1= str(age))
    with driver.session() as session:
        session.write_transaction(insert_vertex_, person_name)

def insert_edges(person_name1, person_name2, driver):
    def insert_edges_(tx, person_name1, person_name2):
        years = random.randint(1,10)
        q2 = "MATCH (a:Person),(b:Person) WHERE a.name=$a_name AND b.name = $b_name CREATE (a)-[r:KNOWS{years:$years1}]-> (b)"  
        tx.run(q2, a_name = str(person_name1), b_name = str(person_name2), years1 = str(years))
        q3 =  "MATCH (a:Person),(b:Person) WHERE a.name=$a_name1 AND b.name=$b_name1 CREATE (b)-[r:KNOWS{years:$years1}] -> (a)" 
        tx.run(q3, a_name1 =str(person_name1), b_name1 = str(person_name2), years1 = str(years))
    with driver.session() as session:
        session.write_transaction(insert_edges_, person_name1, person_name2)

def insert_all_data(lines, driver):

    from time import time
    from tqdm import tqdm

    min_edges = 1000000
    max_edges = 0
    mean_edges = 0
    counter_edges = 2*(len(lines) - 2)

    min_vertices = 1000000
    max_vertices = 0
    mean_vertices = 0
    counter_vertices = 0

    vertex_set = set()
    for line in tqdm(lines, desc = 'tqdm() Progress Bar'):
        
        vertex1 ,vertex2 = line.strip("\n").split(" ")
        
        if vertex1 not in  vertex_set:
            counter_vertices+=1
            vertex_set.add(vertex1)
            time_before = time()
            insert_vertex(vertex1, driver=driver)
            time_after = time()
            diff = time_after - time_before
            max_vertices = max(max_vertices, diff)
            min_vertices = min(min_vertices, diff)
            mean_vertices += diff
        
        if vertex2 not in vertex_set:
            counter_vertices+=1
            vertex_set.add(vertex2)
            time_before = time()
            insert_vertex(vertex2, driver=driver)
            time_after = time()
            diff = time_after - time_before
            max_vertices = max(max_vertices, diff)
            min_vertices = min(min_vertices, diff)
            mean_vertices += diff
        
        time_before = time()
        insert_edges(vertex1, vertex2, driver=driver)
        time_after = time()
        diff = time_after - time_before
        max_edges = max(max_edges, diff/2)
        min_edges = min(min_edges, diff/2)
        mean_edges += diff

    return {
        "edges":{
            "min": min_edges,
            "max": max_edges,
            "mean": mean_edges/counter_edges,
            "total_time": mean_edges
        },
        "vertices":{
            "min": min_vertices,
            "max": max_vertices,
            "mean": mean_vertices/counter_vertices,
            "total_time": mean_vertices
        }
    }  
    
