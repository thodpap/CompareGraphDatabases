def delete_out_edges(person_name, driver):
    def delete_out_edges_(tx, person_name):
        q2 = "MATCH (n:Person{name:$name})-[r:KNOWS]->() DELETE r RETURN r" 
        return len(list(tx.run(q2, name=str(person_name))))
    with driver.session() as session:
        return session.write_transaction(delete_out_edges_, person_name)

def delete_in_edges(person_name, driver):
    def delete_in_edges_(tx, person_name):
        q3 =  "MATCH (n:Person{name:$name}) <-[r:KNOWS]-() DELETE r RETURN r" 
        return len(list(tx.run(q3, name=str(person_name))))
    with driver.session() as session:
        return session.write_transaction(delete_in_edges_, person_name)

def delete_vertex(person_name, driver):
    def delete_vertex_(tx, person_name):
        q3 =  "MATCH (n:Person{name:$name}) DELETE n" 
        tx.run(q3, name=str(person_name))
    with driver.session() as session:
        session.write_transaction(delete_vertex_, person_name)

def delete_vertex_and_its_edges(person_name, driver):
    def delete_vertex_and_its_edges_(tx, person_name):
        q4 = "MATCH (n:Person {name:$name}) DETACH DELETE n" 
        tx.run(q4,name=str(person_name))
    with driver.session() as session:
        session.write_transaction(delete_vertex_and_its_edges_, person_name)

def delete_allnodes(driver):
    def delete_all_nodes_(tx):
        q1 = "MATCH (n) DETACH DELETE n"
        tx.run(q1)
    with driver.session() as session:
        session.write_transaction(delete_all_nodes_)

    
def delete_k_vertices_and_edges(k, driver):
    
    from time import time
    from tqdm import tqdm

    min_edges = 1000000
    max_edges = 0
    mean_edges = 0
    counter_edges = 0

    min_vertices = 1000000
    max_vertices = 0
    mean_vertices = 0
    counter_vertices = k

    for i in tqdm(range(1, k+1), desc = 'tqdm() Progress Bar'):

        time_before_edge = time()
        counter = delete_out_edges(i, driver=driver)
        counter_edges += counter
        time_after_edge = time()
        diff = time_after_edge - time_before_edge
        if counter != 0:
            max_edges = max(max_edges, diff/counter)
            min_edges = min(min_edges, diff/counter)
            mean_edges += diff

        time_before_edges = time()
        counter = delete_in_edges(i, driver=driver)
        counter_edges += counter
        time_after_edges = time()
        diff = time_after_edges - time_before_edges
        if counter != 0:
            max_edges = max(max_edges, diff/counter)
            min_edges = min(min_edges, diff/counter)
            mean_edges += diff

        time_before_vertex = time()
        delete_vertex(i, driver=driver)
        time_after_vertex = time()
        diff = time_after_vertex - time_before_vertex
        max_vertices = max(max_vertices, diff)
        min_vertices = min(min_vertices, diff)
        mean_vertices += diff

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
