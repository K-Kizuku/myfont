# -*- coding: utf-8 -*-
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

from google.cloud import storage

import os 
import glob

from util.font2img       import font2img
from util.img2font       import addfiles
from util.fontgenfromsvg import FontMetaData, generatefont
from util.create_job     import create_custom_job
from util.package        import pickle_examples


# google cloud 上の 使用するコンテナイメージの URI
PROJECT_NAME = "font-generator-365013"
CONTAINER_IMAGE_URI = "asia.gcr.io/font-generator-365013/multiworker@sha256:efbb05d9946eae4f409cd0f4d9ecabd9b780cd4fd34b61459ebb350b958c930c"
BUCKET_NAME = 'font-generator-365013-bucket'


load_dotenv()
CLOUD_NAME  = os.environ.get("CLOUD_NAME")
API_KEY     = os.environ.get("API_KEY")
API_SECRET  = os.environ.get("API_SECRET")
cloudinary.config(
    cloud_name  = CLOUD_NAME,
    api_key     = API_KEY,
    api_secret  = API_SECRET,
)




# データの前処理 と 文字画像の生成
def generate_font_images(
    user_id  = "test@gmail.com",
    data_dir = "/workspace/workspace/data/",
    src_font_name = "meiryob.ttc",
):
    # 各パス
    user_dir        = data_dir +"users/" + user_id +"/"
    user_input_dir  = user_dir + "input/"
    train_obj_path  = os.path.join(user_dir, "train.obj")

    if not os.path.exists(data_dir+"users/"):         
        os.makedirs(data_dir+"users/") 
        print("ディレクトリ"+data_dir+"users/ を作成しました.")


    # 学習データの用意
    data_count = font2img(
        src_font_path   = data_dir + src_font_name,
        user_input_dir  = user_input_dir,
    )

    pickle_examples(sorted(glob.glob(os.path.join(user_input_dir, "*.jpg"))), train_obj_path)

    for img_path in glob.glob(os.path.join(user_input_dir, "*.jpg")):
        os.remove(img_path)

    # データをCloud Storage上にアップロード
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob('datas/'+user_id+'/input/train.obj')
    blob.upload_from_filename(train_obj_path)

    os.remove(train_obj_path)

    # Vertex AI の Train にモデルの訓練/画像生成のjobを依頼
    create_custom_job(
        data_num            = str(data_count), 
        user_name           = user_id, 
        project             = PROJECT_NAME,
        display_name        = "font-generate" ,
        container_image_uri = CONTAINER_IMAGE_URI,
    )


# データの後処理 と フォントデータの取得
def make_font_data(
    user_id  = "test@gmail.com",# 取り出したい フォントデータに対応するユーザーのID
    font_path= "./MyFont.otf",  # 生成したフォントデータを保存する ローカルパス
    data_dir = "/workspace/workspace/data/",    # 画像データやソースフォントデータを入れているディレクトリ
):
    # 各パス
    img_png_dir = data_dir + "users/" + user_id + "/output/png/"
    img_svg_dir = data_dir + "users/" + user_id + "/output/svg/"
    char_list   = data_dir + "charset.json"
    

    # モデルの生成画像を Cloud Storage からダウンロード
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix="datas/"+user_id+"/output/")
    for blob in blobs:
        blob.download_to_filename(img_png_dir + blob.name.split("/")[-1])  
        blob.delete() # ダウンロードしたファイルの削除 



    # 文字画像(ビットマップ) を ベクター画像に変換して保存
    addfiles(img_png_dir, img_svg_dir , char_list)


    font_name = font_path.split("/")[-1]
    # フォントファイルのメタデータ
    metadata = FontMetaData(
        fontname= font_name, 
        family="MyFont", 
        fullname=font_name, 
        weight="Regular", 
        copyrightnotice="generated with FontForge", 
        fontversion="0.01", 
        familyJP=font_name,
        fullnameJP=font_name,
        ascent=860,
        descent=140
    )
    
    # フォント生成
    generatefont(font_path, metadata, img_svg_dir)


if __name__ == "__main__":
    generate_font_images("test@gmail.com")