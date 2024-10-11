import os
import io
import logging
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse
from application.inference import InferenceOnSingleImage
from generateFromText import *

app = FastAPI()

@app.get("/my-first-api", tags=["Check API is working"])
def hello(name: str):
    return('Hello ' + name)

@app.get("/generate-image/from-text", tags=["Comfy generates an image through a text input"])
def generate_from_txt(txt: str):
    text2image(txt)
 
@app.post(f"{endpoint_prefix}/upload_image/", tags=["Test Image upload"])
async def image_file_preview(image_file: UploadFile = File(...)):
    logging.info(image_file.file)
    try:
        os.mkdir("./resources/image_file")
        logging.info(os.getcwd())
    except Exception as e:
        logging.info(e)

    file_path = os.path.join(os.getcwd(), "./resources/image_file", image_file.filename.replace(" ", "-"))
    with open(file_path, 'wb+') as f:
        f.write(image_file.file.read())

    image = Image.open(os.path.join(file_path)).convert('RGB')
    get_caption = InferenceOnSingleImage()
    orig_image, sentence = get_caption.caption_sentence_from_upload(image)
    output = {
        "filename": image_file.filename,
        "predicted_caption": sentence
    }

    image.thumbnail((200, 200))
    buf = io.BytesIO()
    image.save(buf, "JPEG")
    buf.seek(0)
    logging.info(f"Prediction for {image_file} ...done!")
    return StreamingResponse(content=buf, media_type="image/jpeg", headers={"Content-Disposition": f"{output}"});