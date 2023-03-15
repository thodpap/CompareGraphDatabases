curl -X POST http://localhost:8080/graphs/test/ -H "Content-Type:application/json" -d \
'{
gremlin.graph:com.baidu.hugegraph.auth.HugeFactoryAuthProxy,
backend:cassandra,
serializer:cassandra,
store:test
}'
echo ""
