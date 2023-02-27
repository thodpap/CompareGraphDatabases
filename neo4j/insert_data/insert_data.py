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
        q2 = "MATCH (a:Person),(b:Person) WHERE a.name=$a_name AND b.name = $b_name CREATE (a)-[r:Knows{years:$years1}]-> (b)"  
        tx.run(q2, a_name = str(person_name1), b_name = str(person_name2), years1 = str(years))
        q3 =  "MATCH (a:Person),(b:Person) WHERE a.name=$a_name1 AND b.name=$b_name1 CREATE (b)-[r:Knows{years:$years1}] -> (a)" 
        tx.run(q3, a_name1 =str(person_name1), b_name1 = str(person_name2), years1 = str(years))
    with driver.session() as session:
        session.write_transaction(insert_edges_, person_name1, person_name2)

def insert_all_data(lines, driver):
    vertex_set = set()
    for line in lines: 
        
        vertex1 ,vertex2 = line.strip("\n").split(" ")
        
        if vertex1 not in  vertex_set:
            vertex_set.add(vertex1)
            insert_vertex(vertex1, driver=driver)
        
        if vertex2 not in vertex_set: 
            vertex_set.add(vertex2)
            insert_vertex(vertex2, driver=driver)
        
        insert_edges(vertex1, vertex2, driver=driver)
    
