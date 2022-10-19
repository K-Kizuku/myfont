# -*- coding: utf-8 -*-
import os
import pickle

## paths内の画像を ランダムに 訓練用と検証用に分けて それぞれ圧縮(pickled)して保存する
def pickle_examples(paths, train_path):
    with open(train_path, 'wb') as ft:
        for p in paths:
            label = int(os.path.basename(p).split("_")[0])
            with open(p, 'rb') as f:
                print("img %s" % p, label)
                img_bytes = f.read()

                example = (label, img_bytes)
                pickle.dump(example, ft)
