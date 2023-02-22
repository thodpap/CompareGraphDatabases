from neo4j import GraphDatabase
from PyHugeGraph import PyHugeGraphClient

if __name__ == '__main__':
    hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "test")
    print(hg.graph)
    print(hg.clear_graph_alldata().response)
    #name = ID for us, thus name = TEXT for easier HTTP requests to REST API
    print(hg.create_property_key(propertykey_name="name", dataType="TEXT", cardinality="SINGLE").response)
    print(hg.create_property_key(propertykey_name="age", dataType="INT", cardinality="SINGLE").response)
    print(hg.create_property_key(propertykey_name="date", dataType="TEXT", cardinality="SINGLE").response)
    
    data_ = {
        "name": "person",
        "id_strategy": "CUSTOMIZE_STRING",
        "properties": [
            "name",
            "age"
        ],

        "nullable_keys": [],
        "enable_label_index": True
    }
    
    print(hg.create_vertex_label(data=data_).response)

    data_ = {
        "name": "relationship",
        "source_label": "person",
        "target_label": "person",
        "frequency": "SINGLE",
        "properties": [
            "date"
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }

    print(hg.create_edgelabel(data=data_).response)

    data_ = {
        "label": "person",
        "id":"5",
        "properties": {
            "name": "5",
            "age": 29
        }
    }

    print(hg.create_vertex(data=data_).response)
    print(hg.get_vertex_by_id(vertex_id="1").response)


    data_ = {
        "label": "person",
        "id":"2",
        "properties": {
            "name": "2",
            "age": 29
        }
    }
    print(hg.create_vertex(data=data_).response)
    print(hg.get_vertex_by_id(vertex_id="2").response)

    data_ = {
        "date": "2017-5-18"
    }
    print(hg.create_edge(edge_label="relationship", outv="5", inv="2", outv_label="person", inv_label="person", properties=data_).response)
    print(hg.get_edge_by_id(edge_id="S"+str(5)+">1>>S"+str(2)).response)

    data_ = {
        "label": "person",
        "id":"3",
        "properties": {
            "name": "3",
            "age": 30
        }
    }
    print(hg.create_vertex(data=data_).response)
    data_ = {
        "date": "2017-5-19"
    }
    print(hg.create_edge(edge_label="relationship", outv="2", inv="3", outv_label="person", inv_label="person", properties=data_).response)
    print(hg.get_edge_by_id(edge_id="S"+str(2)+">1>>S"+str(3)).response)
    print(hg.update_edge_properties(edge_id="S"+str(5)+">1>>S"+str(2), properties=data_).response)
    print(hg.get_edge_by_id(edge_id="S"+str(5)+">1>>S"+str(2)).response)
    # print(hg.delete_edge_by_id(edge_id="S"+str(5)+">1>>S"+str(2)).response)
    # print(hg.get_edge_by_id(edge_id="S"+str(5)+">1>>S"+str(2)).response)
    data_ = {
        "name": "GetByAge",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "RANGE",
        "fields": [
            "age"
        ]
    }
    print(hg.create_indexlabel(data=data_).response)
    print(hg.delete_vertex_by_id("5").status_code)
    print(hg.get_edge_by_id(edge_id="S"+str(5)+">1>>S"+str(2)).response)
