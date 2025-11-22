// 対象フォルダ選択
inputdirectory = getDirectory("Input directory");

// ファイル名を参照元ディレクトリから配列で取得
filelist = getFileList(inputdirectory);

print("filename, area, circularity, solidity, roundness, major, minor");

// 繰り返し処理
for (n=0; n<filelist.length; n++) {

// イメージファイルを開く
open(inputdirectory + "\\" + filelist[n]);


// マクロ概要：単一ROIから面積・Circularity・Solidity・Roundness・Major・Minorを取得してログ出力

// ファイル名取得
title = getTitle();

// しきい値は必要に応じて調整これは既に2値化している画像が前提で設定済み
minThr = 0;
maxThr = 125;

// 前処理：8-bit化＆選択解除＆ピクセルスケールに統一
run("8-bit");
run("Select None");
run("Set Scale...", "distance=0 known=0 pixel=1 unit=pixel");

// しきい値→マスク→選択作成（ROI生成）
setThreshold(minThr, maxThr);
run("Convert to Mask");
run("Create Selection");

// 測定項目を設定：Area・Circularity・Solidity・Roundness・Major・Minor計算。
// circularityとsolidityは引数にshapeが必要。長径短径にはfitが必要
run("Set Measurements...", "area shape fit redirect=None decimal=3");

// 測定を実行（Resultsテーブルにデータが入る）
run("Measure");

// 測定値をgetValueで取得（最新行の値を参照）
area  = getValue("Area");
circ  = getValue("Circ.");
sol = getValue("Solidity");
roundness = getValue("Round");
major = getValue("Major");
minor = getValue("Minor");

selectWindow(filelist[n]);
close();

// 結果をログ出力
print(title + "," + area + "," + circ + "," + sol + "," + roundness + "," + major + "," + minor);

// すべてのファイルを閉じる
run("Close All");

// 繰り返し処理終了
};
