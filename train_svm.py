# train_svm.py
import os
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib  # モデル保存用
import tkinter as tk
from tkinter import filedialog

# 設定
# IMG_SIZE は固定（ここでは 128x128 → 16384 次元）
IMG_SIZE = (128, 128)      # リサイズサイズ
MODEL_PATH = "ocsvm_model.joblib"  # 保存するモデルファイル名、解析時に読み込むモデルと同一名称にする。


# フォルダ選択ダイアログ
def choose_folder() -> str:
    """
    フォルダ選択ダイアログを表示して、選択されたフォルダパスを返す。
    キャンセルされた場合は空文字列を返す。
    """
    root = tk.Tk()
    root.withdraw()  # ルートウィンドウを表示しない
    folder_selected = filedialog.askdirectory(title="学習用の正常画像フォルダを選択してください")
    root.destroy()
    return folder_selected


# 前処理用関数
def load_image_as_vector(path: str, img_size=(128, 128)) -> np.ndarray:
    """
    1枚の画像を読み込み、グレースケール → リサイズ → 0〜1正規化 → flatten
    """
    img = Image.open(path).convert("L")  # グレースケール
    img = img.resize(img_size)
    arr = np.array(img, dtype=np.float32) / 255.0
    vec = arr.flatten()
    return vec


def load_images_from_folder(folder: str, img_size=(128, 128)) -> np.ndarray:
    """
    フォルダ内の全画像を読み込んで (n_samples, n_features) にする
    """
    folder_path = Path(folder)
    exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

    vectors = []
    for p in folder_path.iterdir():
        if p.suffix.lower() in exts and p.is_file():
            vec = load_image_as_vector(str(p), img_size=img_size)
            vectors.append(vec)

    if not vectors:
        raise ValueError(f"フォルダ {folder} に有効な画像がありません。")

    X = np.stack(vectors, axis=0)
    print(f"読み込んだ正常画像: {X.shape[0]} 枚, 特徴次元: {X.shape[1]}")
    return X


# メイン（学習して保存）
if __name__ == "__main__":
    # 0. 学習用フォルダを選択
    train_dir = choose_folder()
    if not train_dir:
        print("フォルダが選択されませんでした。処理を中止します。")
        exit(0)

    print(f"学習用フォルダ: {train_dir}")

    # 1. 正常画像読み込み
    X_train = load_images_from_folder(train_dir, img_size=IMG_SIZE)

    # 2. StandardScaler + OneClassSVM のパイプライン
    model = make_pipeline(
        StandardScaler(),
        OneClassSVM(kernel="rbf", gamma="auto", nu=0.05)
    )

    print("学習を開始します...")
    model.fit(X_train)
    print("学習が完了しました。")

    # 3. モデルと画像サイズをまとめて保存
    to_save = {
        "model": model,
        "img_size": IMG_SIZE,
    }
    joblib.dump(to_save, MODEL_PATH)
    print(f"モデルを {MODEL_PATH} に保存しました。")
