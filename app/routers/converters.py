"""Router used to convert DataCite XML to opendata.swiss formatted XML."""

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from concurrent.futures import ProcessPoolExecutor, as_completed

import logging

log = logging.getLogger(__name__)

router = APIRouter(prefix="/convert", tags=["convert"])


# TODO finish WIP
# TODO refine annotation
# TODO connect with functionality in parser.py
# TODO organize project structure
@router.post("/datacite-to-opendataswiss")
async def datacite_to_opendataswiss(file: UploadFile):
    return {"filename": file.filename}


# TODO remove
def generate_file():
    """
    Simulate generating a file in chunks and streaming it.
    This could be a process that writes a large file, e.g., a CSV or log file.
    """
    for i in range(10):  # Simulate 10 chunks of data
        chunk = f"Chunk {i + 1}\n".encode("utf-8")
        yield chunk
        # time.sleep(1)  # Simulate some delay in generating the file


# TODO remove
@router.get("/download")
async def download_file():
    """
    Endpoint that streams the file as it is being generated.
    """
    headers = {"Content-Disposition": f"attachment; filename=test.txt"}
    return StreamingResponse(generate_file(), headers=headers)


# TODO remove
def generate_xml_chunks():
    """
    Simulate generating an XML file in chunks and stream it.
    This generates XML content in chunks with tags `<item>`.
    """
    # Start the XML structure
    yield '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'

    for i in range(1, 11):  # Simulate 10 chunks of data
        # Generate an XML element (e.g., <item>...</item>)
        chunk = f"  <item>Item {i}</item>\n"
        yield chunk
        # time.sleep(1)  # Simulate delay in generating each chunk

    # Close the XML structure
    yield "</root>\n"


# TODO remove
@router.get("/download-xml")
async def download_xml():
    """
    Endpoint that streams an XML file while it's being generated.
    """
    headers = {"Content-Disposition": f"attachment; filename=test.xml"}
    return StreamingResponse(generate_xml_chunks(), headers=headers)


# TODO remove
# fastapi write xml file with chunks and streamingresponse with parallelization


# TODO remove
# This doesn't work as expected
def yield_string_chunk(i):
    chunk = f"  <item>Item {i}</item>\n"
    yield chunk


# TODO remove
def create_xml_items(chunk):
    # fixed setup costs to prepare processing, e.g.
    # allocating a resource, like a large file:
    # time.sleep(0.01)
    items = ""
    for i in chunk:
        items += f"  <item>Item {i}</item>\n"
        # time.sleep(0.01)  # short "processing" time
    return items


# TODO remove
def generate_xml_chunks_parallelize():
    """
    Simulate generating an XML file in chunks and stream it.
    This generates XML content in chunks with tags `<item>`.
    """
    # Start the XML structure
    yield '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'

    num_items = 1000
    items = list(range(num_items))

    num_chunks = 8
    chunks = [items[i::num_chunks] for i in range(num_chunks)]

    num_workers = 8
    with ProcessPoolExecutor(num_workers) as executor:
        futures = {executor.submit(create_xml_items, chunk): chunk for chunk in chunks}
        for future in as_completed(futures):
            yield future.result()

    # with ProcessPoolExecutor(num_workers) as executor:
    #     for result in executor.map(create_xml_items, chunks):
    #         yield result

    # with ProcessPoolExecutor(num_workers) as executor:
    #     results = list(executor.map(create_xml_items, chunks))
    # xml_items = "".join(results)
    # yield xml_items

    # xml = ""
    # for chunk in chunks:
    #     xml += create_xml_items(chunk)
    # yield xml

    # for i in range(10):  # Simulate 10 chunks of data
    #     yield f'  <item>Item {i}</item>\n'

    # Close the XML structure
    yield "</root>\n"


# TODO remove
@router.get("/download-xml-parallelize")
async def download_xml_parallelize():
    """
    Endpoint that streams an XML file while it's being generated.
    """
    headers = {"Content-Disposition": f"attachment; filename=test.xml"}
    return StreamingResponse(generate_xml_chunks_parallelize(), headers=headers)
    # return generate_xml_chunks_parallelize()
