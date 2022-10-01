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
    im = Image.fromarray(img_prop)
    im.save("./test.png")
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

if __name__ == "__main__":
    getClondinaryUrl("data:image/png;base64,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","test")
