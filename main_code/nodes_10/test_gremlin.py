import requests

query = "node_10.traversal().V('1:10')"

response = requests.post(
    url="http://localhost:8081/graphs/node_10/jobs/gremlin",
    headers={"Content-Type": "application/json", "Accept": "application/json"},
    json={
        "gremlin": query,
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {}
    }
)

result = response
print(result.content)