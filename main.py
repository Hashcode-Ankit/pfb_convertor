"""
Sample Workflow for Graph-to-PFB Conversion
Steps: Schema Design → Data Conversion → Serialization → Validation → Visualization
"""

import json
from fastavro import writer, reader, parse_schema
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt

# ==================================================================
# Step 1: Define PFB-compliant Avro Schema for Graph Data
# ==================================================================
SCHEMA = {
    "type": "record",
    "name": "GraphData",
    "fields": [
        {"name": "nodes", "type": {"type": "array", "items": {
            "type": "record",
            "name": "Node",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "type", "type": "string"},
                {"name": "properties", "type": {"type": "map", "values": "string"}}
            ]
        }}},
        {"name": "edges", "type": {"type": "array", "items": {
            "type": "record",
            "name": "Edge",
            "fields": [
                {"name": "source", "type": "string"},
                {"name": "target", "type": "string"},
                {"name": "type", "type": "string"},
                {"name": "properties", "type": ["null", {"type": "map", "values": "string"}], "default": None}
            ]
        }}}
    ]
}

parsed_schema = parse_schema(SCHEMA)

# ==================================================================
# Step 2: Sample Graph Data (Replace with real data source)
# ==================================================================
sample_data = {
    "nodes": [
        {"id": "P1", "type": "Patient", "properties": {"age": "35", "gender": "F"}},
        {"id": "D1", "type": "Diagnosis", "properties": {"code": "C50", "description": "Breast Cancer"}},
        {"id": "D2", "type": "Diagnosis", "properties": {"code": "E11", "description": "Diabetes"}}
    ],
    "edges": [
        {"source": "P1", "target": "D1", "type": "HAS_DIAGNOSIS"},
        {"source": "P1", "target": "D2", "type": "HAS_DIAGNOSIS"}
    ]
}

# ==================================================================
# Step 3: Avro Serialization (Conversion to PFB-like format)
# ==================================================================
def write_avro(data: dict, schema: dict) -> bytes:
    buffer = BytesIO()
    writer(buffer, schema, [data])
    buffer.seek(0)
    return buffer.getvalue()

# Serialize sample data
avro_bytes = write_avro(sample_data, parsed_schema)

# ==================================================================
# Step 4: Validate Deserialization
# ==================================================================
def read_avro(data: bytes, schema: dict) -> dict:
    buffer = BytesIO(data)
    return next(reader(buffer, schema))

deserialized_data = read_avro(avro_bytes, parsed_schema)
print("Deserialized Data Validation:")
print(json.dumps(deserialized_data, indent=2))

# ==================================================================
# Step 5: Basic Visualization (Optional)
# ==================================================================
def visualize_graph(data: dict):
    G = nx.Graph()
    
    # Add nodes
    for node in data["nodes"]:
        G.add_node(node["id"], type=node["type"], **node["properties"])
    
    # Add edges
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], label=edge["type"])
    
    # Draw
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'label')
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

visualize_graph(deserialized_data)