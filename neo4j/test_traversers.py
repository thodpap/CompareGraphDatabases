import traversers
from neo4j import GraphDatabase


uri = "bolt://localhost:7687"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

traversers.shortest_path(7, 3, driver)