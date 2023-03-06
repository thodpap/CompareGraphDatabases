from update_data import update_data
from neo4j import GraphDatabase

uri = "bolt://localhost:7690"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

#update_data.update_vertex(person_name=1, driver=driver)
#update_data.update_out_edges(person_name=1, driver=driver)
print(update_data.update_all_data(10, driver))
driver.close()