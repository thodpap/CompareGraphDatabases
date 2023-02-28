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
    batched_list1 =[]
    for i in range(1, number_of_vertices, batch_size):
    
        batched_list = []
        for j in range(i, min(i+batch_size, number_of_vertices+1)):
            batch ={}
            batch['name'] = str(j)
            batch['age'] = str(random.randint(1,100))
            batched_list.append(batch)
        batched_list1.append(batched_list)
        
        batch_insert_nodes(batched_list, driver)
   

def batch_in_edges(number_of_edges, batch_size, driver):
    import random
    vertices_rels = []

    for line in number_of_edges: 
        vertex1, vertex2 = line.strip("\n").split(" ")
        vertices_rels.append((vertex1,vertex2))

    for i in range(0, len(number_of_edges), batch_size):
        batched_list = []
        for j in range(i,min(i+batch_size,len(number_of_edges))):
            batch = {}
            batch['from'] = vertices_rels[j][0]
            batch['to'] = vertices_rels[j][1]
            batch['properties'] ={'years':str(random.randint(1,10))}
            batched_list.append(batch)
        batch_insert_in_rels(batched_list, driver)
        batch_insert_out_rels(batched_list, driver)

