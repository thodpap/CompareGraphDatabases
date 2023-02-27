from neo4j import GraphDatabase
from insert_data import insert_data
from read_data import read_data
from delete_data import delete_all_data
uri = "bolt://localhost:7687"
username = "neo4j"
password = "trial2"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Create a session for executing queries
with driver.session() as session:
    
        
    result = session.run("MATCH (n:Person{name: '1'}) RETURN n")
    records = list(result)
    # Process the results of the query
    for record in records:
        print(record)
        
# Close the driver when you're done with it
driver.close()