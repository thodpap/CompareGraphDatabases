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
    for i in range(1, number_of_vertices+1, batch_size):
        batched_list =  []
        for j in range(i, min(i+batch_size, number_of_vertices+1)):
                batch ={}
                batch['name'] = str(j)
                batch['age'] = str(random.randint(1,100))
                batched_list.append(batch)
        batch_update_nodes(batched_list, driver)

def update_update_e(number_of_edges, batch_size, driver):
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
            batch_up_in_edges(batched_list, driver)
            batch_up_out_edges(batched_list, driver)