def delete_out_edges(person_name, driver):
    def delete_out_edges_(tx, person_name):
        q2 = "MATCH (n:Person{name:$name})-[r:Knows]->() DELETE r" 
        tx.run(q2,name=str(person_name))
    with driver.session() as session:
        session.write_transaction(delete_out_edges_, person_name)


def delete_in_edges(person_name, driver):
    def delete_in_edges_(tx, person_name):
        q3 =  "MATCH (n:Person{name:$name})<-[r:Knows]-() DELETE r" 
        tx.run(q3, name=str(person_name))
    with driver.session() as session:
        session.write_transaction(delete_in_edges_, person_name)

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

    

