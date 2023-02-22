import requests

query = "g.V('1')"

response = requests.post(
    url="http://localhost:8080/graphs/node_1000/jobs/gremlin",
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
