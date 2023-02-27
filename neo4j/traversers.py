def shortest_path(person_name1, person_name2, driver):
    q1 = "MATCH (a:Person {name:$a_name}), (b:Person {name:$b_name}), p = shortestPath((a)-[:Knows*]-(b)) RETURN nodes(p) "
    with driver.session() as session:
        shortestPath = session.run(q1, a_name = str(person_name1), b_name = str(person_name2))
        records = list(shortestPath)
        print(records)


