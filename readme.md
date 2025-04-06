# Graph Data To Avro Convertor
In this module we are trying to convert graph data to PFB format

# Local Setup 
- Create Virtual Environment 
    ```bash
    python -m venv .venv
    ```
- Activate Virtual Env
    ```bash
    source .venv/bin/activate
    ```
- Install requirements 
    ```bash
    pip install -r requirements.txt
    ```
- Run Main
    ```bash
    python main.py
    ```

# Key Components:

- Schema Definition: PFB-like schema supporting nodes and edges

- Data Conversion: Simple in-memory dictionary → Avro serialization

- Validation: Round-trip serialization/deserialization check

- Visualization: Basic NetworkX graph visualization

# Output:

- Serialized Avro data (PFB-like format)

- Validated deserialized data printed to console

- Interactive graph visualization