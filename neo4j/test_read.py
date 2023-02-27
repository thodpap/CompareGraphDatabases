from neo4j import GraphDatabase
from read_data import read_data

uri = "bolt://localhost:7687"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Create a session for executing queries)
# read_data.read_vertex(person_name=1, driver=driver)
# read_data.read_out_edges_of_vertex(person_name=1, driver=driver)
print(read_data.read_all_data(n=10, driver=driver))
        
driver.close()