from io import BytesIO
from dotenv import load_dotenv
import base64
import numpy as np
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image
from fastapi import HTTPException
import os 
import cv2

load_dotenv()
CLOUD_NAME = os.environ.get("CLOUD_NAME")
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
cloudinary.config(
    cloud_name = CLOUD_NAME,
    api_key = API_KEY,
    api_secret = API_SECRET,
    secure = True
)

def getClondinaryUrl(img_text: str, user_id: str) -> str:
    img_text_sprited = img_text.split(",")
    if len(img_text_sprited) != 2:
        raise HTTPException(status_code=400,detail="image text uncollect")

    img_text_data = img_text_sprited[-1]
    #バイナリデータ <- base64でエンコードされたデータ
    img_binary = base64.b64decode(img_text_data)
    temp = np.array(Image.open(BytesIO(img_binary)))

    img_prop = []
    for x in temp:
        tmp = []
        for y in x:
            tmp.append(255 - y[3]) # Aの値を抽出して白黒反転
        img_prop.append(tmp)
    img_prop = np.array(img_prop).astype("uint8")
    cv2.imwrite("./test.png",img_prop)
    res = cloudinary.uploader.upload(file="./test.png", unique_filename=True, tags=user_id)
    return res["url"]


def deleteImage(user_id: str):
    pids = []
    target_images = cloudinary.Search().expression('tags={}'.format(user_id)).max_results(100).execute()
    for image in target_images["resources"]:
        pids.append(image["public_id"])
    while len(pids) != 0:
        cloudinary.api.delete_resources(public_ids=pids)
        pids = []
        target_images = cloudinary.Search().expression(
            "tags={}".format(user_id)).max_results(100).execute()
        for image in target_images["resources"]:
            pids.append(image["public_id"])
    return
