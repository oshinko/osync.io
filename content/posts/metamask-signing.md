+++
date = "2018-06-19T18:00:00+09:00"
draft = false
title = "MetaMask Signing"
tags = ["MetaMask", "Ethereum"]
image = "/images/headers/metamask.png"
+++

MetaMask を介したメッセージ署名を行いました。

## MetaMask を準備

MetaMask は Chrome 拡張機能です。下記からダウンロードください。

[![MetaMask](/images/metamask-dl.png)](https://metamask.io/)

## HTML を作成

MetaMask が用意した Ethereum web3 API を実行する HTML ファイルを作成します。

```bash
cat <<EOF> metamask-signing.html
<!DOCTYPE html>
<html>
  <head>
    <title>MetaMask Signing</title>
  </head>
  <body>
    <textarea id="address" placeholder="Address" readonly></textarea>
    <textarea id="message" placeholder="Message"></textarea>
    <textarea id="sign" placeholder="Sign" readonly></textarea>
    <style>
      textarea {
        display: block;
        margin: .8em;
        width: 40em;
        height: 10em;
        max-width: 100%;
      }
    </style>
    <script>
      var web3 = new Web3(web3.currentProvider);
      var address = document.getElementById('address');
      var current = null;
      var refresh = setInterval(function() {
        if (web3.eth.defaultAccount !== current) {
          address.value = current = web3.eth.defaultAccount;
        }
      }, 100);
      var sign = document.getElementById('sign');
      document.getElementById('message').addEventListener('blur', function() {
        if (this.value) {
          var hex = web3.toHex(this.value);
          var from = web3.eth.defaultAccount;
          web3.personal.sign(hex, from, (e, r) => sign.value = r);
        }
      }, false);
    </script>
  </body>
</html>
EOF
```

## サーバーを起動

Web サーバーはなんでもいいのですが、 Python 3 の http.server モジュールを利用するのが楽です。

```bash
python3 -m http.server
```

## ブラウザで確認

[ブラウザで確認](/docs/metamask-signing.html)すると MetaMask を介して署名をすることが出来ると思います。

MetaMask のアンロックを忘れずに！
