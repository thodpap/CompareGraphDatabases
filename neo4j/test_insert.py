from insert_data import insert_data
from neo4j import GraphDatabase

uri = "bolt://localhost:7690"
username = "neo4j"
password = "node_10node_10"
driver = GraphDatabase.driver(uri, auth=(username, password))

file1 = open("node_10.txt", 'r')
lines = file1.readlines()[2:]

print(insert_data.insert_all_data(lines=lines, driver=driver))

with driver.session() as session:
    session.run("CREATE FULLTEXT INDEX PersonName FOR (n:Person) ON EACH [n.name]")

driver.close()