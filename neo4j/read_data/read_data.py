def read_vertex(person_name, driver):
    def read_vertex_(tx , person_name):
        q1 = "MATCH (n:Person{name:$name}) RETURN n"
        result = tx.run(q1, name=str(person_name))
        # records = list(result)
        # print(records)
    with driver.session() as session:
        session.read_transaction(read_vertex_, person_name)


def read_out_edges_of_vertex(person_name, driver):
    def read_out_edges_of_vertex_(tx, person_name):
        q2 = "MATCH (n:Person{name:$name})-[r:Knows]->(b:Person) RETURN  r"
        result = tx.run(q2, name=str(person_name))
        # records = list(result)
        #print(records)
    with driver.session() as session:
        session.read_transaction(read_out_edges_of_vertex_, person_name)



def read_all_data(n, driver):
    for i in range(1,n+1):
        read_vertex(i, driver)
        read_out_edges_of_vertex(i, driver)

        