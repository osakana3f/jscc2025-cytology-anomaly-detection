# batch_predict_svm.py
import os
from pathlib import Path

import numpy as np
from PIL import Image
import joblib
import tkinter as tk
from tkinter import filedialog
import csv


# 設定
MODEL_PATH = "ocsvm_model.joblib"  # train_svm.py で保存したモデル


# 前処理関数（学習時と同じ条件にする）
def load_image_as_vector(path: str, img_size=(128, 128)) -> np.ndarray:
    """
    1枚の画像を読み込み、グレースケール → リサイズ → 0〜1正規化 → flatten
    """
    img = Image.open(path).convert("L")
    img = img.resize(img_size)
    arr = np.array(img, dtype=np.float32) / 255.0
    vec = arr.flatten()
    return vec


# フォルダ選択ダイアログ
def choose_folder() -> str:
    """
    フォルダ選択ダイアログを表示して、選ばれたパスを返す
    """
    root = tk.Tk()
    root.withdraw()  # ルートウィンドウを表示しない
    folder_selected = filedialog.askdirectory(title="判定したい画像フォルダを選択してください")
    root.destroy()
    return folder_selected


# フォルダ内一括判定
def batch_predict(model_dict_path: str, folder: str):
    """
    保存済みモデルを読み込み、指定フォルダ内の全画像を一括で判定する
    結果はコンソール表示 + CSVに保存
    """
    # 1. モデル読み込み
    loaded = joblib.load(model_dict_path)
    model = loaded["model"]
    img_size = loaded["img_size"]

    folder_path = Path(folder)
    exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

    results = []

    print(f"判定フォルダ: {folder_path}")
    print("画像ファイルを探索中...\n")

    for p in sorted(folder_path.iterdir()):
        if p.suffix.lower() in exts and p.is_file():
            try:
                vec = load_image_as_vector(str(p), img_size=img_size)
                vec = vec.reshape(1, -1)

                pred = model.predict(vec)[0]             # 1: 正常, -1: 異常
                score = model.decision_function(vec)[0]  # 大きいほど正常寄り

                if pred == 1:
                    label = "NORMAL（正常）"
                else:
                    label = "ANOMALY（異常）"

                results.append((p.name, label, score))
            except Exception as e:
                print(f"[エラー] {p.name} の処理中に問題が発生しました: {e}")

    if not results:
        print("有効な画像ファイルが見つかりませんでした。")
        return

    # 2. コンソールに一覧表示
    print("\n=== 判定結果 ===")
    for filename, label, score in results:
        print(f"{filename}\t{label}\tスコア: {score:.4f}")

    # 3. CSVに保存
    csv_path = folder_path / "svm_prediction_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label", "score"])
        for filename, label, score in results:
            writer.writerow([filename, label, f"{score:.6f}"])

    print(f"\n結果を CSV に保存しました: {csv_path}")


# メイン
if __name__ == "__main__":
    # モデルが存在するか確認
    if not os.path.exists(MODEL_PATH):
        print(f"モデルファイル {MODEL_PATH} が見つかりません。先に train_svm.py を実行して学習してください。")
        exit(1)

    # 判定フォルダの選択
    folder = choose_folder()
    if not folder:
        print("フォルダが選択されませんでした。処理を中止します。")
        exit(0)

    # 一括判定
    batch_predict(MODEL_PATH, folder)
