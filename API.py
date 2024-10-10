from fastapi import FastAPI
from generateFromText import *

app = FastAPI()

@app.get("/my-first-api")
def hello(name: str):
    return('Hello ' + name)

@app.get("/generate-image/from-text")
def generate_from_txt(txt: str):
    text2image(txt)