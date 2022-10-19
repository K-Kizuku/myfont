# -*- coding: utf-8 -*-
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import glob


## フォントデータfont で 文字ch を書く処理
def draw_single_char(ch, font, canvas_size, x_offset, y_offset):
    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font, anchor='mm')
    return img


## dst_char_img は ユーザーが書いた手書き文字の画像
def draw_example(src_font, dst_char_img_path, canvas_size, x_offset, y_offset):
    dst_img = Image.open(dst_char_img_path)
    ch = os.path.splitext(os.path.basename(dst_char_img_path))[0][0]

    src_img = draw_single_char(ch, src_font, canvas_size, x_offset, y_offset)
    
    # どちらかの文字が 白紙(文字chに フォントが対応していない)場合
    if src_img.getextrema() == ((255,255),(255,255),(255,255)) :
        return None
    
    example_img = Image.new("RGB", (canvas_size * 2, canvas_size), (255, 255, 255))
    example_img.paste(dst_img, (0, 0))
    example_img.paste(src_img, (canvas_size, 0))
    
    return example_img


## モデルをユーザーの手書き文字に寄せるための 学習データを作る関数
def font2img(
    src_font_path: str, user_input_dir: str,
    output_image_size   = 256,
    x_offset            = 128,
    y_offset            = 128,
    output_embedding_id = 39,
):
    src_font = ImageFont.truetype(src_font_path, size=150)
    label = output_embedding_id
    count = 0

    for img_path in glob.glob(os.path.join(user_input_dir,"*.png")):
        e = draw_example(src_font, img_path, output_image_size, x_offset, y_offset)
        if e:
            e.save(os.path.join(user_input_dir, "%d_%04d.jpg" % (label, count)))
            os.remove(img_path)
            count += 1

    return count