+++
date = "2018-08-11T19:00:00+09:00"
draft = false
title = "HTTP Ethereum Authentication"
tags = ["http", "ethereum", "auth"]
image = "/images/headers/http-ethereum-auth.jpg"
+++

Ethereum アドレスを検証する HTTP 認証スキームです。

具体的な実装は、 [Python パッケージ](https://github.com/oshinko/pyhttpauth)で確認できます。

## 使い方

仕様はシンプルで、次のようにアドレスと署名を Authorization ヘッダに記述することにより、検証および認証を行います。

```bash
curl -X POST -H "Authorization: Ethereum $ADDR $SIGN" \
     http://localhost:8080/ethereum/addresses
```

## 動作確認

実際に簡単なサーバーを作っていきます。

事前に `osnk.httpauth` と `osnk.validations` をインストールしてください。

```bash
python -m pip install -U -e git+https://github.com/oshinko/pyvalidation.git#egg=validation
python -m pip install -U -e git+https://github.com/oshinko/pyhttpauth.git#egg=httpauth
```

[Flask](http://flask.pocoo.org) を使って作っていきます。
他のお好みのフレームワークでもいいと思います。

```
cat <<EOF> run.py
from flask import Flask, jsonify, request
from osnk.httpauth import EthereumAuthentication
from osnk.validations import requires

app = Flask(__name__)
eth_auth = EthereumAuthentication()


@eth_auth.authorization
def authorization(header):
    return request.headers.get(header)


@eth_auth.authenticate
def authenticate(header, scheme):
    return jsonify(error='Unauthorized'), 401, {header: scheme}


@eth_auth.message
def message(address):
    return b'Hello!'


@app.route('/ethereum/addresses', methods=['POST'])
@requires(eth_auth)
def post_ethereum_addresses():
    return jsonify(f'0x{eth_auth.address.hex()}')


@app.route('/')
def get_client():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Client</title>
</head>
<body>
  <script>
    var web3 = new Web3(web3.currentProvider);
    var current = null;
    setInterval(() => {
      if (web3.eth.defaultAccount !== current) {
        current = web3.eth.defaultAccount;
        var hex = web3.toHex("Hello!");
        var from = web3.eth.defaultAccount;
        web3.personal.sign(hex, from, (e, r) => {
          if (e) {
            var result = document.createTextNode(e.message);
            document.querySelector("body").appendChild(result);
            return;
          }
          var req = new XMLHttpRequest();
          req.open("POST", "/ethereum/addresses");
          req.setRequestHeader("Content-Type", "application/json");
          req.setRequestHeader("Authorization", \`Ethereum \${from} \${r}\`);
          req.onreadystatechange = () => {
            if (req.readyState === 4 && req.status === 200) {
              var address = JSON.parse(req.responseText);
              var result = document.createTextNode(\`Accepted \${address}.\`);
              document.querySelector("body").appendChild(result);
            }
          };
          req.send();
        });
      }
    }, 100);
  </script>
</body>
</html>
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
EOF
```

サーバーを起動します。

```
python run.py
```

スクリプト実行後、 [localhost:8080](http://localhost:8080) にアクセスすると動作確認ができます。

以上、 Ethereum Address の所有権の証明をする上での参考になればと思います。
