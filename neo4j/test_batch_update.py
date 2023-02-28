import batch_update
from neo4j import GraphDatabase


uri = "bolt://localhost:7687"
username = "neo4j"
password = "node_100node_100"
driver = GraphDatabase.driver(uri, auth=(username, password))

file1 = open("node_100.txt", 'r')
lines = file1.readlines()[2:]

batch_update.batch_update_n(100, 10, driver)
batch_update.update_update_e(lines, 100, driver)

driver.close()




