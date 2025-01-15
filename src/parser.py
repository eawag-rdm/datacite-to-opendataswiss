import zipfile


# TODO finish WIP
# TODO improve docstring
# TODO specify return type as zip with xml files in return hint and docstring,
#  consider error return types
# TODO consider using a size limit to prevent memory issues or process items in chunks
# TODO consider implementing multiprocessing to improve performance
# TODO add parameter that specifies which schema will be used for conversion,
#  designate a default schema
def parse_zipfile(file_path: str):
    """
    Parse XML files in an input zipfile.

    Args:
        file_path (str): path to zipfile.
    """
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, "r") as zf:
            has_xml = False

            for filename in zf.namelist():
                if filename.endswith(".xml"):
                    has_xml = True
                    print(filename)  # TODO remove
                    # TODO call conversion logic

            if not has_xml:
                # TODO improve error handling
                print(
                    f"Input '{file_path}' does not have a file with an '.xml' "
                    f"extension."
                )
    else:
        # TODO improve error handling
        print(f"Input '{file_path}' is not a zip file.")
