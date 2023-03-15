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
        q2 =  "MATCH (a:Person {name:$a_name})-[r:KNOWS]-> (b:Person{name:$b_name}) SET r.years = $years RETURN r"
        tx.run(q2, a_name=person_name1, b_name=person_name2, years=str(years1))
        q3 = "MATCH (a:Person {name:$a_name}) <-[r:KNOWS]- (b:Person{name:$b_name}) SET r.years = $years RETURN r"
        tx.run(q3, a_name=person_name1, b_name=person_name2, years = str(years1))
    with driver.session() as session:
        session.write_transaction(update_edge_, person_name1, person_name2)


def update_out_edges(person_name, driver):
    def update_out_edges_(tx, person_name):
        q4 = "MATCH (n:Person{name:$name})-[r:KNOWS]->(b:Person) SET  r.years = toInteger(round(rand()*10)) RETURN r"
        return len(list(tx.run(q4, name= str(person_name))))
    with driver.session() as session:
        return session.write_transaction(update_out_edges_ , person_name)


def update_all_data(n, driver):

    from time import time
    from tqdm import tqdm

    min_edges = 1000000
    max_edges = 0
    mean_edges = 0
    counter_edges = 0

    min_vertices = 1000000
    max_vertices = 0
    mean_vertices = 0
    counter_vertices = n

    for i in tqdm(range(1, n+1), desc = 'tqdm() Progress Bar'):

        time_before_vertex = time()
        update_vertex(i, driver)
        time_after_vertex = time()
        time_before_edge = time()
        counter = update_out_edges(i, driver)
        counter_edges += counter
        time_after_edge = time()

        diff_vertices = time_after_vertex - time_before_vertex
        diff_edges = time_after_edge - time_before_edge

        max_vertices = max(max_vertices, diff_vertices)
        min_vertices = min(min_vertices, diff_vertices)
        mean_vertices += diff_vertices
        if counter != 0:
            max_edges = max(max_edges, diff_edges/counter)
            min_edges = min(min_edges, diff_edges/counter)
            mean_edges += diff_edges

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