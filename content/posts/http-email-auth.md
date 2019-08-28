+++
date = "2018-07-21T22:30:00+09:00"
draft = false
title = "HTTP Email Authentication"
tags = ["HTTP", "Email", "Auth"]
image = "/images/headers/http-email-auth.jpg"
+++

Email を利用した HTTP 認証スキームです。

メールによるワンタイムパスワードなど、パスワードレス認証の実現を目的とした、 HMAC ベースのテンポラリトークン認証スキームとなっています。

具体的な実装は、 [Python パッケージ](https://github.com/oshinko/pyhttpauth)で確認できます。

## 認証を開始する

`POST /email/auth` が認証を開始する API と仮定します。

HTTP リクエストと同時に、本文にパスワードを含んだメールが送信されます。

```bash
$ curl -v -d '["me@domain"]' http://localhost:8080/email/auth
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /email/auth HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.54.0
> Accept: */*
> Content-Length: 13
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 13 out of 13 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 71
< Server: Werkzeug/0.14.1 Python/3.7.0
< Date: Sat, 21 Jul 2018 11:00:05 GMT
< 
"BFtTJNUNWyJtZUBkb21haW4iXV9ord26MiebdfzlAtj6+cU6huRLELVo3og6NeFHfHcP"
* Closing connection 0
```

レスポンスボディには、 Hint と呼ばれるトークンが含まれます。

Hint を環境変数に設定するには、次のようなコマンドを実行します。

```bash
HINT=`curl -d '["me@domain"]' http://localhost:8080/email/auth | sed -e 's/^"//' -e 's/"$//'`
```

## アクセストークンを取得する

次に、メールに送信された認可情報を提示して、アクセストークンを取得します。

認可情報は、 Authorization ヘッダにあるように、メールアドレスとパスワードの組み合わせに `POST /email/auth` で得た Hint を加えた情報です。

`GET /email/token` が、その役割を担う API と仮定します。

```bash
$ ADDR=`echo -n me@domain | base64`
$ PASS=`echo -n $RECEIVED_PASSWORD | base64`
$ curl -v -H "Authorization: Email $ADDR $PASS $HINT" http://localhost:8080/email/token
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /email/token HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
> Authorization: Email bWVAZG9tYWlu WERPRUFSU1FRSlA1 BFtTJNUNWyJtZUBkb21haW4iXV9ord26MiebdfzlAtj6+cU6huRLELVo3og6NeFHfHcP
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 71
< Server: Werkzeug/0.14.1 Python/3.7.0
< Date: Sat, 21 Jul 2018 11:22:48 GMT
< 
"BFtTJZgNWyJtZUBkb21haW4iXbr2VN4a4l0+wARNQSuyx7AldqU6V9PEojuqHxmCUmD9"
* Closing connection 0
```

メールアドレスとパスワードは、任意のデータを許容する目的で Base64 エンコードを施します。

アクセストークンを環境変数に設定するには、次のようなコマンドを実行します。

```bash
TOKEN=`curl -H "Authorization: Email $ADDR $PASS $HINT" http://localhost:8080/email/token | sed -e 's/^"//' -e 's/"$//'`
```

## Hint について

Hint は、認証を開始してからの有効期限と、ユーザー任意のペイロード、認可情報の HMAC 署名を含むトークンです。

メールアドレスに送信されるパスワードをサーバーの秘密鍵で暗号化したデータであり、これを参照して認証を行います。

次の疑似コードは、 Hint の作成例です。

```
Secret = "Your secret words"
Address = "me@domain"
Password = RANDOM()
Expires = "2018-01-01T00:00:00"
Payload = "Hello!"
Answer = Address + " " + Password + " " + Expires + " " + Payload
Signature = HMACSHA256(Secret, Answer)
Hint = BASE64(Expires + Payload + Signature)
```

## 認証により保護されたリソースにアクセスする

最後に、保護されたリソースにアクセスする一例を示します。

メール認証によって得られたアクセストークンをサーバーに提示することで、アクセス権を証明します。

```bash
$ curl -v -H "Authorization: Email-Token $TOKEN" http://localhost:8080/locked/contents
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /locked/contents HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.54.0
> Accept: */*
> Authorization: Email-Token BFtTPhgNWyJtZUBkb21haW4iXbhKH/OE+DIYewHWFsiAZpL9zPgybYZDm423EhPzrzDT
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 29
< Server: Werkzeug/0.14.1 Python/3.7.0
< Date: Sat, 21 Jul 2018 13:07:30 GMT
< 
{
  "welcome": "me@domain"
}
* Closing connection 0
```

以上、メール認証によって証明されたアドレスの所有権がないと取得できない情報や、操作できない機能を実装する上での参考になればと思います。
