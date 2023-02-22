from PyHugeGraph import PyHugeGraphClient

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8080", "node_1000")

print(hg.create_property_key(propertykey_name="name", dataType="TEXT", cardinality="SINGLE").response)
print(hg.create_property_key(propertykey_name="age", dataType="INT", cardinality="SINGLE").response)
print(hg.create_property_key(propertykey_name="strong", dataType="INT", cardinality="SINGLE").response)

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
        "strong"
    ],
    "sort_keys": [],
    "nullable_keys": [],
    "enable_label_index": True
}

print(hg.create_edgelabel(data=data_).response)
