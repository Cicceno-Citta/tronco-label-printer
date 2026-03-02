import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .core import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    output_folder = settings.OUTPUT_FOLDER
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Created output folder at {output_folder}")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class PrintLabelRequest(BaseModel):
    mynumber: str
    name: str


@app.post("/print-label")
async def print_label(request: PrintLabelRequest):
    output_folder = settings.OUTPUT_FOLDER
    file_path = os.path.join(output_folder, f"{request.mynumber}.csv")
    if os.path.exists(file_path):
        return {"message": "Label already exists"}
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{request.mynumber}, {request.name}\n")
    return {"message": "Label queued for printing successfully"}


@app.get("/print-list")
async def print_list():
    output_folder = settings.OUTPUT_FOLDER
    files = []
    for filename in os.listdir(output_folder):
        if filename.endswith(".csv"):
            files.append(filename.removesuffix(".csv"))
    return {"files": files}
