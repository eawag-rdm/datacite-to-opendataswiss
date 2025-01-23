from io import BytesIO
import xml.etree.ElementTree as ElemTree

import zipfile

# TODO remove
import time
script_start_time = time.perf_counter()


# TODO remove
def modify_xml_content(xml_content, tag_replacement, text_replacement):
    """
    Modify the XML content by replacing tags and text.

    Args:
        xml_content (bytes): Original XML file content.
        tag_replacement (dict): A dictionary mapping old tags to new tags.
        text_replacement (dict): A dictionary mapping old text to new text.

    Returns:
        bytes: Modified XML content as bytes.
    """
    try:
        # Parse the XML content
        tree = ElemTree.ElementTree(ElemTree.fromstring(xml_content))
        root = tree.getroot()

        # Change tags
        for elem in root.iter():
            # Replace tag names
            if elem.tag in tag_replacement:
                elem.tag = tag_replacement[elem.tag]

            # Replace text content
            if elem.text and elem.text.strip() in text_replacement:
                elem.text = text_replacement[elem.text.strip()]

        # Write the modified XML content to bytes
        modified_xml = BytesIO()
        tree.write(modified_xml, encoding="utf-8", xml_declaration=True)
        return modified_xml.getvalue()
    except Exception as e:
        print(f"Error modifying XML content: {e}")
        return None


# TODO finish WIP
# TODO improve docstring
# TODO specify return type as zip with xml files in return hint and docstring,
#  consider error return types
# TODO consider using a size limit to prevent memory issues or process items in chunks
# TODO consider implementing ProcesspoolExecutor to improve performance
# TODO add parameter that specifies which schema will be used for conversion,
#  designate a default schema
# TODO log error messages, see websnap for setting up logging
def parse_zipfile(input_path: str):
    """
    Parse XML files in an input ZIP file.

    Args:
        input_path (str): path to input ZIP file.
    """
    if zipfile.is_zipfile(input_path):

        # TODO remove
        tag_replacement = {"note": "message", "to": "receiver", "from": "sender"}
        text_replacement = {"old_text": "new_text",
                            "Example content": "Updated content"}

        with zipfile.ZipFile(input_path, "r") as zip_in:
            has_xml = False
            namelist = zip_in.namelist()

            # TODO modify and create root elements with a function
            # Create the root element for the aggregated XML
            root = ElemTree.Element("AggregatedData")

            for file_name in namelist:
                if file_name.endswith(".xml"):
                    has_xml = has_xml or True
                    # print(file_name)  # TODO remove

                    with zip_in.open(file_name) as file:
                        input_xml = file.read()

                        # TODO remove
                        modified_xml = modify_xml_content(input_xml,
                                                          tag_replacement,
                                                          text_replacement)
                        modified_xml_bytes = ElemTree.fromstring(modified_xml)
                        root.append(modified_xml_bytes)

                        # TODO call conversion logic

            if not has_xml:
                # TODO improve error handling
                print(
                    f"Input '{input_path}' does not have a file with an '.xml' "
                    f"extension."
                )

            # Write the aggregated XML to a memory buffer
            buffer = BytesIO()
            tree = ElemTree.ElementTree(root)
            tree.write(buffer, encoding="utf-8", xml_declaration=True)

            # Return the combined XML as bytes
            buffer.seek(0)
            return buffer.getvalue()

    else:
        # TODO improve error handling
        print(f"Input '{input_path}' is not a zip file.")


# TODO remove
# Tests
# zip_content = parse_zipfile("doi_wsl.zip")
# with open("example.xml", "wb") as f:
#     f.write(zip_content)

# TODO remove
script_end_time = time.perf_counter()
print(f"Total script execution time: {script_end_time - script_start_time:.6f} seconds")
