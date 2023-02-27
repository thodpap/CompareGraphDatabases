import random 

def update_vertex(person_name, driver):
    def update_vertex_(tx, person_name):
        age1 = random.randint(1, 100) 
        q1 = "MATCH (n:Person{name:$name}) SET n.age=$age RETURN n"
        tx.run(q1, name=str(person_name), age=str(age1))
    with driver.session() as session:
        session.write_transaction(update_vertex_, person_name)



def update_edge(person_name1, person_name2, driver):
    def update_edge_(tx, person_name1, person_name2):
        years1 = random.randint(1, 10)
        q2 =  "MATCH (a:Person {name:$a_name})-[r:Knows]-> (b:Person{name:$b_name}) SET r.years = $years RETURN r"
        tx.run(q2, a_name=person_name1, b_name=person_name2, years=str(years1))
        q3 = "MATCH (a:Person {name:$a_name}) <-[r:Knows]- (b:Person{name:$b_name}) SET r.years = $years RETURN r"
        tx.run(q3, a_name=person_name1, b_name=person_name2, years = str(years1))
    with driver.session() as session:
        session.write_transaction(update_edge_, person_name1, person_name2)


def update_out_edges(person_name, driver):
    def update_out_edges_(tx, person_name):
        q4 = "MATCH (n:Person{name:$name})-[r:Knows]->(b:Person) SET  r.years = toInteger(round(rand()*10)) RETURN r"
        tx.run(q4, name= str(person_name))
    with driver.session() as session:
        session.write_transaction(update_out_edges_ , person_name)


def update_all_data(n,driver):
     for i in range(1, n+1):
         update_vertex(i, driver)
         update_out_edges(i, driver)
