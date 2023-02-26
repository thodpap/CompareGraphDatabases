import requests
# property("stong", 11).property("FromTo", "20 -> 10")
query = 'node_100000.traversal().V(1:1).outE()'

response = requests.get(
    url="http://localhost:8081/gremlin?gremlin=" + query,
)

result = response
print(response.status_code)
# print(eval(result.content))


