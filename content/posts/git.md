+++
date = "2018-06-15T20:00:00+09:00"
draft = false
title = "Git インストール"
tags = ["git"]
image = "/images/headers/git.png"
+++

ソースコードからインストールする方法です。

OS は Linux や macOS を想定しています。

```install-git.sh
git clone git@github.com:git/git.git
cd git
make configure
./configure --prefix=/usr/local/git
sudo make install
git --version
```

ライブラリ依存エラーが発生する場合は、別途調べてみてください。
