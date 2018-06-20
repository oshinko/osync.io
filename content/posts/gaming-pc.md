+++
date = "2018-05-12T12:00:00+09:00"
draft = false
title = "ゲーミング PC"
tags = ["Ryzen", "Gaming", "PC", "Machine",
        "Cryptocurrency", "Mining", "PUBG"]
image = "/images/headers/gaming-pc.png"
+++

PUBG やりたかったので、ゲーミングマシンを組みました。

Specs:

- CPU: AMD Ryzen 7 2700X
- Motherboard: ASRock X470 Taichi Ultimate
- RAM: F4-2933C14D-32GTZRX (DDR4 PC4-23400 16GB x 2)
- OS: Windows 10 Home
- Storage: Samsung SSD 500GB 960EVO
- GPU: ZOTAC GeForce GTX 1080 Ti AMP Extreme
- Power: Seasonic SSR-850TR
- Chassis: CA-1J7-00M1WN-01 VIEW 37 RGB Plus
- Mouse: Logicool G903 + G-PMP-001
- Keyboard: HyperX Alloy FPS Pro HX-KB4RD1-US/R1
- Chair: DXRACER DXZ-BLN
- LAN: KB-T7ME-02BKR

## Windows 10 がインストールできない問題

[Windows 10 ディスクイメージ ISO ファイル](https://www.microsoft.com/ja-jp/software-download/windows10ISO)から、
ブータブル USB を作成してインストールを試みましたが、失敗してしまった問題を共有します。

### 症状

ブータブル USB を挿し込み、正常に起動したかのように見えますが、下記のドライバーインストール画面で止まります。

![Windows 10 インストール失敗](/images/win10-driver-not-found.png "Windows 10 インストール失敗")

この問題を解決するために、まず最初に考えられるドライバーのインストールや BIOS 設定を試しましたが、全く効果がみられませんでした。

### 原因

作成したブータブル USB 自体に問題がありました。

私は Mac 端末の diskutil コマンドを使用しましたが、何か異常な状態で作成されてしまうようで、 Windows 7 以上の端末にて、公式で用意される Windows 10 メディア作成ツールで作り直して試したところ、あっさり上手くいきました。

## PUBG がクラッシュする問題

こちらはさらにしんどい問題。ゲームの起動後にクラッシュが頻発し、まともに遊べません。

### 症状

ゲームの起動後、ロビー画面クラッシュ、マッチングクラッシュ、降下中クラッシュ、激戦区クラッシュ、安地外クラッシュ、とにかくゲームがよく落ちます。復帰して運良くキャラが生きてた時は感動します。予め想定して、安地方向に走らせてクラッシュに備えるんですよ。マジで辛かったです。

### 原因 (回避策)

これといった原因は未だ不明ですが、色々と試行錯誤した結果、現在は解決して普通に遊べています。

ただし、完全に安定させるには、フレームレートを 60 fps に固定する必要がありました。

効果が見られた方法がこちらです。

1. PUBG グラフィック品質を全て「最低」にすると多少安定
2. PUBG グラフィック設定の垂直同期を有効にして、フレームレートを固定すると完全に安定 (下記の画像)

![PUBG グラフィック設定](/images/pubg-settings-20180522.png "PUBG グラフィック設定")

この 2 番目の方法を試すまで、ゲームカメラを激しく動かすとモニタに若干のティアリングが生じていました。
もしかするとグラフィックボードの性能と比較して、使用しているモニタの最大リフレッシュレートが
60Hz と低いことが影響しているかもしれません。

リフレッシュレートの高いゲーム向きモニタに変えたら、垂直同期を無効にしてもクラッシュせずにグラフィックボードの性能を引き出せるのかな？

後日、この辺りを検証したいと思っています。

### 効果がなかった方法

一応、効果がなかった方法についても記載しておきます。

効果がなかったとはいえ、主要モジュールのテストが出来たので、複雑な気分ではありますw

- GPU ドライバーを再インストール (GeForce Experience)
- GPU 検査 (MSI Kombustor Stress Test 問題なし)
- GPU グラフィックボードの挿し直し (別 PCIe スロットへの挿し直し含む)
- メモリ検査 (Memtest86 で 5 Pass)
- SSD 検査 (CrystalDiskMark 問題なし)
- [ASRock BIOS アップデート](https://www.asrock.com/MB/AMD/X470%20Taichi%20Ultimate/index.jp.asp#BIOS)
- Steam Overlay を無効
- GeForce Experience Overlay を無効
- PUBG グラフィック品質を全て「低」に設定

## 仮想通貨マイニング性能

Ryzen 7 2700X で Yescrypt マイニング試したところ、ハッシュレート 8 KH/s ほど出ました。
流石のパワーです。
GPU マイニングは後日検証して、こちらに記載したいと思います。
