def read_vertex(person_name, driver):
    def read_vertex_(tx , person_name):
        q1 = "MATCH (n:Person{name:$name}) RETURN n"
        tx.run(q1, name=str(person_name))
    with driver.session() as session:
        session.read_transaction(read_vertex_, person_name)


def read_out_edges_of_vertex(person_name, driver):
    def read_out_edges_of_vertex_(tx, person_name):
        q2 = "MATCH (n:Person{name:$name})-[r:KNOWS]->(b:Person) RETURN  r"
        return len(list(tx.run(q2, name=str(person_name))))
    with driver.session() as session:
        return session.read_transaction(read_out_edges_of_vertex_, person_name)


def read_all_data(n, driver):

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

    for i in tqdm(range(1,n+1), desc = 'tqdm() Progress Bar'):

        time_before_vertex = time()
        read_vertex(i, driver)
        time_after_vertex = time()
        diff = time_after_vertex - time_before_vertex
        max_vertices = max(max_vertices, diff)
        min_vertices = min(min_vertices, diff)
        mean_vertices += diff

        time_before_edges = time()
        counter = read_out_edges_of_vertex(i, driver)
        counter_edges += counter
        time_after_edges = time()
        diff = time_after_edges - time_before_edges
        if counter_edges != 0:
            max_edges = max(max_edges, diff/counter)
            min_edges = min(min_edges, diff/counter)
            mean_edges += diff

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