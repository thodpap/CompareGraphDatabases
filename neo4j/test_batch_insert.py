import batch_insert
from neo4j import GraphDatabase
import random

uri = "bolt://localhost:7687"
username = "neo4j"
password = "node_100node_100"
driver = GraphDatabase.driver(uri, auth=(username, password))

file1 = open("node_100.txt", 'r')
lines = file1.readlines()[2:]


batch_insert.batch_in_nodes(100, 10 , driver)
batch_insert.batch_in_edges(lines, 100, driver)



driver.close()