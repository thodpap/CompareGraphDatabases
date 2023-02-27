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
    delete_all_data.delete_allnodes(session)
    file1 = open("10_nodes.txt", 'r')
    lines = file1.readlines()[2:]
    vertex_set = set()
    for line in lines: 
    
        vertex1 ,vertex2 = line.strip("\n").split(" ")
    
        if vertex1 not in  vertex_set:
            vertex_set.add(vertex1)
            insert_data.insert_vertex(vertex1, session)
    
        if vertex2 not in vertex_set: 
            vertex_set.add(vertex2)
            insert_data.insert_vertex(vertex2, session)
    
        insert_data.insert_edges(vertex1, vertex2,session)
        
    #result = session.run("MATCH (n:Person{name: '1'}) RETURN n")
    #records = list(result)
    # Process the results of the query
    #for record in records:
     #   print(record)
        
# Close the driver when you're done with it
driver.close()