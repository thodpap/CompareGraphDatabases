def batch_insert_nodes(insert_list, driver):
    def batch_insert_nodes_(tx, insert_list):
        q1 = "UNWIND $batch as row CREATE (n:Person) SET n +=row "
        tx.run(q1,batch = insert_list)
    with driver.session() as session:
        session.write_transaction(batch_insert_nodes_, insert_list)


def batch_insert_out_rels(insert_rels, driver):
    def batch_insert_rels_(tx, insert_rels):
        q1 = "UNWIND $batch as row MATCH (from:Person {name: row.from}) MATCH (to:Person {name: row.to}) CREATE (from)-[r:KNOWS]->(to)  SET r += row.properties"
        tx.run(q1,batch = insert_rels)
    with driver.session() as session:
        session.write_transaction(batch_insert_rels_, insert_rels)
    
def batch_insert_in_rels(insert_rels, driver):
    def batch_insert_rels_(tx, insert_rels):
        q2 = "UNWIND $batch as row MATCH (from:Person {name: row.from}) MATCH (to:Person {name: row.to}) CREATE (from)<-[r:KNOWS]-(to)  SET r += row.properties"
        tx.run(q2,batch = insert_rels)
    with driver.session() as session:
        session.write_transaction(batch_insert_rels_, insert_rels)


def batch_in_nodes(number_of_vertices, batch_size, driver):
    
    import random
    from time import time
    from tqdm import tqdm

    min_vertices = 1000000
    max_vertices = 0
    mean_vertices = 0
    counter_vertices = number_of_vertices

    batched_list1 =[]
    for i in tqdm(range(1, number_of_vertices, batch_size), desc = 'tqdm() Progress Bar'):
    
        batched_list = []
        temp_counter = 0
        for j in range(i, min(i+batch_size, number_of_vertices+1)):
            batch ={}
            batch['name'] = str(j)
            batch['age'] = str(random.randint(1,100))
            batched_list.append(batch)
            temp_counter += 1
        batched_list1.append(batched_list)
        
        time_before = time()
        batch_insert_nodes(batched_list, driver)
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
   

def batch_in_edges(lines, batch_size, driver):
    
    import random
    from time import time
    from tqdm import tqdm

    length = len(lines)

    min_edges = 1000000
    max_edges = 0
    mean_edges = 0
    counter_edges = 2*length
    vertices_rels = []

    for line in lines: 
        vertex1, vertex2 = line.strip("\n").split(" ")
        vertices_rels.append((vertex1,vertex2))

    for i in tqdm(range(0, length, batch_size), desc = 'tqdm() Progress Bar'):
        
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
        batch_insert_in_rels(batched_list, driver)
        batch_insert_out_rels(batched_list, driver)
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

def batch_insert(number_of_vertices, batch_size_vertices, lines, batch_size_edges, driver):

    vertices = batch_in_nodes(number_of_vertices=number_of_vertices, batch_size=batch_size_vertices, driver=driver)
    edges = batch_in_edges(lines=lines, batch_size=batch_size_edges, driver=driver)
    
    return {
        "vertices": vertices,
        "edges": edges
    }