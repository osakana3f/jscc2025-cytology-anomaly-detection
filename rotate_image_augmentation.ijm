//対象フォルダ選択
inputdirectory = getDirectory("Input directory");

//ファイル名を参照元ディレクトリから配列で取得
filelist = getFileList(inputdirectory);

//繰り返し処理
for (n=0; n<filelist.length; n++) {

	//プロセス開始
	print("Start Process: "+filelist[n]);

	//イメージファイルを開く
	open(inputdirectory + "\\" + filelist[n]);

//----
// ★元画像の情報取得
origTitle = getTitle();
origPath  = getDirectory("image"); 

// ★拡張子と名前を分離
dotIndex = lastIndexOf(origTitle, ".");
baseName = substring(origTitle, 0, dotIndex);
ext      = substring(origTitle, dotIndex); 

// ===== 90°回転して保存 =====
run("Rotate 90 Degrees Right");
saveAs("Tiff", origPath + baseName + "_90" + ".tif");

// ===== 180°回転して保存 =====
run("Rotate 90 Degrees Right"); // 90° → 180°へ
saveAs("Tiff", origPath + baseName + "_180" + ".tif");

// ===== 270°回転して保存 =====
run("Rotate 90 Degrees Right"); // 180° → 270°へ
saveAs("Tiff", origPath + baseName + "_270" + ".tif");

// ===== 画像を閉じる =====
close();
//----

//すべてのファイルを閉じる
	run("Close All");

	//プロセス終了確認
	print("End Process: "+filelist[n]);
};
