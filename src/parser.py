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
# TODO consider implementing multiprocessing to improve performance
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

        with BytesIO() as zip_buffer:
            # TODO research ZIP_DEFLATED
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_output:

                # TODO remove
                # Read the original ZIP file into memory
                # with open(input_path, "rb") as f:
                #     zip_data = f.read()

                # with zipfile.ZipFile(BytesIO(zip_data), "r") as zip_in:  # TODO remove
                with zipfile.ZipFile(input_path, "r") as zip_in:
                    has_xml = False
                    namelist = zip_in.namelist()

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
                                zip_output.writestr(file_name, modified_xml)
                                # TODO call conversion logic

                    if not has_xml:
                        # TODO improve error handling
                        print(
                            f"Input '{input_path}' does not have a file with an '.xml' "
                            f"extension."
                        )

            # Make sure the buffer is ready to be read
            zip_buffer.seek(0)

            return zip_buffer.getvalue()
    else:
        # TODO improve error handling
        print(f"Input '{input_path}' is not a zip file.")


# Tests
zip_content = parse_zipfile("doi_wsl.zip")
with open("example.zip", "wb") as f:
    f.write(zip_content)

# TODO remove
script_end_time = time.perf_counter()
print(f"Total script execution time: {script_end_time - script_start_time:.6f} seconds")
