+++
date = "2023-07-24T09:00:00+09:00"
draft = false
title = "代表取締役の引っ越し手続き"
tags = ["法人", "引っ越し", "eLTAX"]
image = "/images/headers/beautiful-nature-20230504.jpg"
+++

代表取締役 (社長, CEO, 法人の代表者) の引っ越しに関する手続きについて、個人的な備忘録です。

## 大まかな流れ

1. 変更登記申請 (To: 法務局)
1. 異動届出書の提出 (To: 税務署等)
1. 変更届の提出 (To: 年金事務所)

## 変更登記申請

- 提出先: 法務局 (例えば、会社の本店が渋谷なら東京法務局渋谷出張所に出す)
- [手続きについて](https://houmukyoku.moj.go.jp/homu/touki2.html)
- 電子申請の方法
  1. 「[登記・供託オンライン申請システム 登記ねっと 供託ねっと](https://www.touki-kyoutaku-online.moj.go.jp/)」とかいう馬鹿みたいな名前のサイトでアカウント登録
      - 「[申請者情報登録](https://www.touki-kyoutaku-online.moj.go.jp/web/top/SC01WL01-RegistShinseisha.do)」からアカウント登録できる
      - [平日 8:30 - 21:00 まで](https://www.touki-kyoutaku-online.moj.go.jp/condition.html)しか使えない (意味分からん)
  1. [「申請用総合ソフト」のインストール](https://www.touki-kyoutaku-online.moj.go.jp/download.html)
  1. 申請書に情報を記入・作成する
      - クソヤバ UI のアコーディオンカテゴリツリー

        ```txt
        ├ 不動産登記申請書
        ├ 商業登記申請書
        │   └ 登記申請書【署名要】
        │       └ 登記申請書（会社用）：株式会社，...【署名要】
        │           └ 色々入力して「株式会社変更登記申請書」様式に辿り着け！
        ├ ...
        ```

  1. 代表者のマイナンバーカードで申請書を電子署名
  1. 「登録免許税 = 30,000 円、または資本金が 1 億円以下の場合 10,000 円」を納付

## 異動届出書の提出

- 提出先: 税務署 (国税), 都道府県税事務所, 市区町村
- 様式は、提出先の三種類ともほぼ同一

### 税務署への提出

- [手続きについて](https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/annai/1554_5.htm)
- 税務署は国税なので e-Tax でできる
  1. 法人で e-Tax 登録
  1. 「利用者情報の登録...」から、代表者のマイナンバーカードを登録する
  1. 「申告・申請・納税」から、異動手続きの申請をする

### 都道府県税事務所への提出

- 地方税管轄なので eLTAX でできる
  1. 法人で eLTAX 登録
  1. 代表者のマイナンバーカードを登録
  1. 申請する

### 市区町村への提出

- 会社の管轄税務署が東京 23 区であれば、都税事務所へ提出するだけでいいので、提出の必要はない
- eLTAX でできそう
- もしかしたら、普通徴収だと出す必要ないかも？

## 年金事務所へ変更届の提出

次の二種類がある:

1. 健康保険・厚生年金保険事業所関係変更届
1. 健康保険・厚生年金保険被保険者住所変更届

両方とも [e-Gov](https://www.nenkin.go.jp/denshibenri/index.html) で電子申請できるが、法人の電子証明書がないといけない。

[認証局のご案内 | e-Gov電子申請](https://shinsei.e-gov.go.jp/contents/preparation/certificate/certification-authority.html)

上記のリンクから電子証明書の発行方法を調べると、発行手数料を確認できる:

有効期間|手数料
--|--
3 ヶ月|¥1,300
6 ヶ月|¥2,300
9 ヶ月|¥3,300
12 ヶ月|¥4,300
15 ヶ月|¥5,300
18 ヶ月|¥6,300
21 ヶ月|¥7,300
24 ヶ月|¥8,300
27 ヶ月|¥9,300

クソ高いので郵送する。なぜ、未だにマイナンバーカードによる電子署名を採用していないのか理解できない。

### 健康保険・厚生年金保険事業所関係変更届

1. 「[事業主の変更や事業所に関する事項の変更（訂正）があったとき](https://www.nenkin.go.jp/service/kounen/todokesho/jigyosho/20150212.html)」を開く
1. 様式のエクセルファイルをダウンロード
1. ファイルを開き、情報を記入する
    - [健康保険被保険者整理番号（年金整理番号）とは](https://jobcan-lms.zendesk.com/hc/ja/articles/360000966532)
    - [事業所整理記号と健康保険証「記号」の変換方法](https://gozal.cc/basics/symbol-of-company-for-koseinenkin)
1. ファイルをクラウドとかに保管する
1. ファイルを印刷する
1. [全国の事務センター一覧 (郵送先)](https://www.nenkin.go.jp/service/kounen/todokesho/20150216.html) を参照し、封筒に宛先を書く
1. 印刷物を封筒に入れ、[切手を貼る](https://www.post.japanpost.jp/send/fee/kokunai/one_two.html)
1. ポストに投函する

### 健康保険・厚生年金保険被保険者住所変更届

[被保険者の住所に変更があったとき](https://www.nenkin.go.jp/service/kounen/todokesho/kankeitodoke/20150513.html)

> マイナンバーと基礎年金番号が結びついていない被保険者が住所変更を行う場合には届出が必要

アンチマイナ勢なら前述の手順でわざわざ郵送しましょう。
