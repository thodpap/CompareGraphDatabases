from delete_data import delete_data
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

# print(delete_data.delete_k_vertices_and_edges(k=10, driver=driver))
print(delete_data.delete_allnodes(driver))
# delete_data.delete_vertex_and_its_edges(person_name=1, driver=driver)
# delete_data.delete_in_edges(person_name=2, driver=driver)
# delete_data.delete_out_edges(person_name=2, driver=driver)

driver.close()