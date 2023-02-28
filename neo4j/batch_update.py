def batch_update_nodes(update_list, driver):
    def batch_update_nodes_(tx, update_list):
        q1 = "UNWIND $batch AS row MATCH (n:Person) WHERE n.name = row.name SET n.age = row.age RETURN n "
        tx.run(q1, batch = update_list)
    with driver.session() as session:
        session.write_transaction(batch_update_nodes_, update_list)


def batch_up_in_edges(up_list, driver):
    def batch_up_in_edges_(tx, up_list):
        q2 = "UNWIND $batch AS row MATCH (a:Person{name:row.from}) MATCH (b:Person{name:row.to})  MATCH (a)-[r:KNOWS]->(b)  SET r += row.properties"
        tx.run(q2, batch = up_list)
    with driver.session() as session:
        session.write_transaction(batch_up_in_edges_, up_list)

def batch_up_out_edges(up_list, driver):
    def batch_up_out_edges_(tx, up_list):
        q2 = "UNWIND $batch AS row MATCH (a:Person) WHERE a.name = row.from MATCH (b:Person) WHERE b.name = row.to  MATCH (a)<-[r:KNOWS]-(b)  SET r += row.properties"
        tx.run(q2, batch = up_list)
    with driver.session() as session:
        session.write_transaction(batch_up_out_edges_, up_list)


def batch_update_n(number_of_vertices, batch_size, driver):
    
    import random
    from time import time

    min_vertices = 1000000
    max_vertices = 0
    mean_vertices = 0
    counter_vertices = number_of_vertices

    for i in range(1, number_of_vertices+1, batch_size):

        batched_list =  []
        temp_counter = 0
        for j in range(i, min(i+batch_size, number_of_vertices+1)):
            batch ={}
            batch['name'] = str(j)
            batch['age'] = str(random.randint(1,100))
            batched_list.append(batch)
            temp_counter += 1

        time_before = time()
        batch_update_nodes(batched_list, driver)
        time_after = time()
        diff = time_after - time_before
        mean_vertices += diff
        max_vertices = max(max_vertices, diff/temp_counter)
        min_vertices = min(min_vertices, diff/temp_counter)

    return {
        "min": min_vertices,
        "max": max_vertices,
        "mean": mean_vertices/counter_vertices,
        "total_time": mean_vertices
    }

def batch_update_e(lines, batch_size, driver):
    
    import random
    from time import time

    length = len(lines)

    min_edges = 1000000
    max_edges = 0
    mean_edges = 0
    counter_edges = 2*length
    vertices_rels = []
    vertices_rels = []

    for line in lines: 
        vertex1, vertex2 = line.strip("\n").split(" ")
        vertices_rels.append((vertex1,vertex2))

    
    for i in range(0, length, batch_size):

        batched_list = []
        temp_counter = 0
        for j in range(i,min(i+batch_size, length)):
            batch = {}
            batch['from'] = vertices_rels[j][0]
            batch['to'] = vertices_rels[j][1]
            batch['properties'] ={'years':str(random.randint(1,10))}
            batched_list.append(batch)
            temp_counter += 2

        time_before = time()
        batch_up_in_edges(batched_list, driver)
        batch_up_out_edges(batched_list, driver)
        time_after = time()
        diff = time_after - time_before
        mean_edges += diff
        max_edges = max(max_edges, diff/temp_counter)
        min_edges = min(min_edges, diff/temp_counter)

    return {
        "min": min_edges,
        "max": max_edges,
        "mean": mean_edges/counter_edges,
        "total_time": mean_edges
    }

def batch_update(number_of_vertices, batch_size_vertices, lines, batch_size_edges, driver):

    vertices = batch_update_n(number_of_vertices=number_of_vertices, batch_size=batch_size_vertices, driver=driver)
    edges = batch_update_e(lines=lines, batch_size=batch_size_edges, driver=driver)
    
    return {
        "vertices": vertices,
        "edges": edges
    }