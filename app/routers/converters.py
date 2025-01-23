"""Router used to convert DataCite XML to opendata.swiss formatted XML."""

from fastapi import APIRouter, UploadFile

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
