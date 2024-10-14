import os
import io
import logging
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from websocketTest import *
from generateFromText import *

app = FastAPI()

@app.get("/my-first-api", tags=["Check API is working"])
def hello(name: str):
    return('Hello ' + name)

@app.get("/generate-image/from-text", tags=["Comfy generates an image through a text input"])
def generate_from_txt(txt: str):
    text2image(txt)
 
@app.post("/uploadfile/", tags=["Check Image workflow"])
async def create_upload_file(file: UploadFile):
    generateImage(file)