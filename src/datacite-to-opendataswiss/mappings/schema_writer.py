from genson import SchemaBuilder
import json


def json_schema_writer(input_json_path: str, output_json_path: str):
    """
    Generate and write JSON schema from input JSON file.

    Args:
        input_json_path (str): Path to input JSON file.
        output_json_path (str): Path to output JSON file.

    Returns:
        None: None.
    """
    try:
        with open(input_json_path, "r") as file:
            data = json.load(file)

        builder = SchemaBuilder()
        builder.add_object(data)
        schema = builder.to_schema()

        with open(output_json_path, "w") as json_file:
            json.dump(schema, json_file, indent=4)

    except Exception as e:
        raise Exception(f"Failed to write schema from input JSON file: {e}")
