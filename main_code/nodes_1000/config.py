from PyHugeGraph import PyHugeGraphClient

hg = PyHugeGraphClient.HugeGraphClient("http://localhost", "8081", "node_10")

print(hg.create_property_key(propertykey_name="name", dataType="TEXT", cardinality="SINGLE").response)
print(hg.create_property_key(propertykey_name="age", dataType="INT", cardinality="SINGLE").response)
print(hg.create_property_key(propertykey_name="strong", dataType="INT", cardinality="SINGLE").response)
print(hg.create_property_key(propertykey_name="FromTo", dataType="TEXT", cardinality="SINGLE").response)

data_ = {
        "name": "person",
        "properties": [
            "name",
            "age"
        ],
        "primary_keys": [
            "name"
        ],
        "id_strategy": "PRIMARY_KEY",
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
        "strong",
        "FromTo"
    ],
    "sort_keys": [],
    "nullable_keys": [],
    "enable_label_index": True
}

print(hg.create_edgelabel(data=data_).response)

data_ = {
    "name": "relatioshipFromTo",
    "base_type": "EDGE_LABEL",
    "base_value": "relationship",
    "index_type": "SECONDARY",
    "fields": [
        "FromTo"
    ]
}
print(hg.create_indexlabel(data=data_).response)

data_ = {
    "name": "personName",
    "base_type": "VERTEX_LABEL",
    "base_value": "person",
    "index_type": "SECONDARY",
    "fields": [
        "name"
    ]
}
print(hg.create_indexlabel(data=data_).response)