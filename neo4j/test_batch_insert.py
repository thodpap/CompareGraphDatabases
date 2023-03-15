import batch_insert
from neo4j import GraphDatabase


uri = "bolt://localhost:7690"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

file1 = open("node_10.txt", 'r')
lines = file1.readlines()[2:]


# batch_insert.batch_in_nodes(100, 10 , driver)
# print(list1)
# batch_insert.batch_in_edges(lines, 100, driver)

print(batch_insert.batch_insert(number_of_vertices=10, batch_size_vertices=1000, lines=lines, batch_size_edges=1000, driver=driver))

driver.close()