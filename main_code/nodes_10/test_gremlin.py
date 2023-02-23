import requests
# property("stong", 11).property("FromTo", "20 -> 10")
query = 'node_10.traversal().V("1:20").as("20").V("1:21").as("21").addE("relationship").from("21").to("20").property("strong", 10).property("FromTo", "21 -> 20")'

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
print(eval(result.content)["task_id"])