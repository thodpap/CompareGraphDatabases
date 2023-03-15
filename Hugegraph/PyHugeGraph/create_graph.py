# from neo4j import GraphDatabase
from PyHugeGraph import PyHugeGraphClient

if __name__ == '__main__':

    import argparse
    import requests
    import json

    token = "162f7848-0b6d-4faf-b557-3a0797869c55"
    conform_message = "I%27m+sure+to+delete+all+data"

    url = "http://localhost:8080/graphs/hugegraph2?token=" + token
    graph_name = "hugegraph2"
    backend_ = "cassandra"
    serializer_ = "cassandra"
    data_ = {
        "gremlin.graph":"com.baidu.hugegraph.auth.HugeFactoryAuthProxy",
        "backend":backend_, 
        "serializer":serializer_,
        "store":graph_name,
        "cassandra.host":"localhost",
        "cassandra.port":"9042",
        "cassandra.username":"",
        "cassandra.password":"",
        "cassandra.connect_timeout":"5",
        "cassandra.read_timeout":"20",
        "cassandra.keyspace.strategy":"SimpleStrategy",
        "cassandra.keyspace.replication":"3"

    }
    auth_ = ("", "")
    # headers_ = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    #                       '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    #         'Content-Type': 'application/json'
    #     }
    headers_ = {
        "Content-Type":"application/json"
    }

    
# json=data_, , auth=auth_
    res = requests.post(url=url, data=data_, headers=headers_)
    print(res.content)


