第64回日本臨床細胞学会秋期大会で発表した「口腔粘膜上皮性異形成と扁平上皮癌における核形態に関する細胞学的及び組織学的検」に使用したコードです。
公開しているコードは以下の４つです。

１）rotate_image_augmentation.ijm

２）train_svm.py

３）predict_anomaly.py

４）nuclear_morphometry.ijm

１）rotate_image_augmentation.ijm

90、180、270度回転させデータ拡張を行うコードです。指定したフォルダ内の画像を読み込み90、180、270度回転させた画像を新たに作成し同一フォルダに追加します。

２）train_svm.py

scikit-learnのOneClassSVMを使用したトレーニング用コードです。指定したフォルダ内の画像を教師データとして読み込み学習モデルをカレントディレクトリに保存します。

３）predict_anomaly.py

トレーニングによって得られた学習モデルを使用して指定したフォルダ内の画像を一括判定するコードです。OneClassSVMを使用しているため0を下回っている場合に異常と判定されます。

４）nuclear_morphometry.ijm

2値化済みの核形態の解析を行うコードです。area, circularity, solidity, roundness, major axis, minor axisを算出します。関心領域（核）を黒（0,0,0）に非関心領域（核以外の領域）を白（255,255,255）で塗りつぶした2値画像を予め作製しておく必要があります。
