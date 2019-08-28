+++
date = "2018-06-22T16:00:00+09:00"
draft = false
title = "Ethereum Hello World Contract"
tags = ["Ethereum", "Solidity"]
image = "/images/headers/solidity.png"
+++

この記事では、実際のスマートコントラクト (DApps) を [Hello World Contract チュートリアル](https://www.ethereum.org/greeter)に沿って動かしています。

事前に [Ethereum プライベートネットを構築](/posts/ethereum-private-network/)しておくと、ブロック同期や Gas 支払いのために使われる Ether を採掘する待ち時間が短くなり、ストレスを溜めずに進められます。

## コントラクトを定義

まず最初に Greeter というコントラクトを `Greeter.sol` ファイルに定義していきます。

Greeter は、他の誰かに挨拶するためのコントラクトです。予め決めたメッセージで初期化したオブジェクトを、誰かが `greet` 関数を呼び出すことでメッセージを取得できます。

```bash
cat <<EOF> Greeter.sol
pragma solidity ^0.4.24;

/* 自己破棄可能なコントラクト */
contract Mortal {
    /* コントラクト所有者のアドレス */
    address owner;

    /* 初期化時に呼ばれる関数 */
    constructor() public {
        owner = msg.sender;  // 所有者を設定
    }

    /* 自己破棄する関数 */
    function kill() public {
        if (msg.sender == owner) {
            // コントラクトに格納された Ether を回収した後、
            // ストレージとコードを削除する。
            selfdestruct(owner);
        }
    }
}

/* 挨拶コントラクト */
contract Greeter is Mortal {
    /* メッセージ */
    bytes32 greeting;

    /* 初期化時に呼ばれる関数 */
    constructor(bytes32 _greeting) public {
        greeting = _greeting;  // メッセージを設定
    }

    /* メッセージを取得する関数 */
    function greet() public view returns (bytes32) {
        return greeting;
    }
}
EOF
```

Mortal は、 `kill` 関数による自己破棄可能なコントラクトで、この特性は Greeter に継承されます。所有者だけが `kill` 関数を呼び出すことが出来ます。コントラクトが必要なくなった時にブロックチェーンを掃除し、資金を回収する目的があります。これを定義しないと展開した後に破棄することが出来ないので、実装を検討してください。

## コンパイル

次の二つの方法があります。

- Solidity コンパイラを使用する
- Web ベースの Solidity IDE である Remix を使用する

### Solidity コンパイラを使用する

Solidity コンパイラの `solc` を使用するため、[ドキュメント](https://github.com/ethereum/solidity)に従いビルドします。

次のシェルスクリプトは、ドキュメントのリンク先にある、ソースコードからのビルド手順をまとめたものです。

```bash
git clone --recursive https://github.com/ethereum/solidity.git
cd solidity
git checkout v0.4.24  # Select from `git tag -l`
./scripts/install_deps.sh
./scripts/build.sh
solc  # Show help message
```

`homebrew` の入っていない macOS の場合は、次のようにビルドします。

#### Installing Boost on macOS

```bash
curl -OL https://dl.bintray.com/boostorg/release/1.66.0/source/boost_1_66_0.tar.gz
tar xzf boost_1_66_0.tar.gz
cd boost_1_66_0
./bootstrap.sh
sudo ./b2 install --prefix=/usr/local/boost
```

#### Installing Solidity on macOS

```bash
git clone --recursive https://github.com/ethereum/solidity.git
cd solidity
git checkout v0.4.24  # Select from `git tag -l`
sudo BOOST_ROOT=/usr/local/boost scripts/build.sh
solc  # Show help message
```

`Greeter.sol` をコンパイルします。

```bash
solc -o target --bin --abi Greeter.sol
```

次のように target というディレクトリに .abi (Application Binary Interface) と .bin が作成されます。

```bash
tree
.
├── Greeter.sol
└── target
    ├── Greeter.abi
    ├── Greeter.bin
    ├── Mortal.abi
    └── Mortal.bin
```

実際に Geth コンソールを起動し、コントラクトを作成してみます。Greeter には Mortal が含まれているため、 Greeter を展開するために Mortal を作成する必要はありません。

```javascript
var greeterFactory = eth.contract(...);  // Greeter.abi の内容を渡す
var greeterCompiled = "0x" + "...";      // Greeter.bin の内容を渡す
```

展開する前にアカウントをアンロックします。

```javascript
personal.unlockAccount(eth.accounts[0], '');
```

作成したコントラクトをネットワークへ展開します。 `Contract mined! Address` と表示されれば成功です。

```javascript
var _greeting = "Hello World!"

var greeter = greeterFactory.new(_greeting, {from: eth.accounts[0], data: greeterCompiled, gas: 4700000}, function(e, contract) {
    if (e) {
      console.error(e);  // If something goes wrong, at least we'll know.
      return;
    }
    if (!contract.address) {
      console.log("Contract transaction send: TransactionHash: " + contract.transactionHash + " waiting to be mined...");
    } else {
      console.log("Contract mined! Address: " + contract.address);
      console.log(contract);
    }
});
```

### Remix を使用する

`solc` をインストールしていない場合は、 [Remix](https://remix.ethereum.org/) を使用します。

コントラクトの作成・展開の手順は次の通りです。

1. ソースコード `Greeter.sol` を Remix にコピーして、コンパイルされることを確認
2. 右ペインのドロップダウンメニューで **Greeter** が選択されていることを確認
3. ドロップダウンの右にある **Details** ボタンをクリック
4. ポップアップを下にスクロールして **WEB3DEPLOY** の内容をコピー
5. `yourFilename.js` を作成し、コピーしたコードをペースト
6. ローカル開発環境での作業

#### Remix での作業

`selfdestruct` に関する警告が出ると思いますが、呼び出し元チェックにより安全とみなし、無視しています。

![Remix での作業](/images/remix-compile.png)

#### ローカル開発環境での作業

`yourFilename.js` の最初の行を次のように変更してください。

```javascript
var _greeting = "Hello World!";
```

`geth` コンソールを起動して、アカウントをアンロックします。

```javascript
personal.unlockAccount(eth.accounts[0], '');
```

スクリプトを読み込んでコントラクトを作成・展開します。

```javascript
loadScript("yourFilename.js");
```

マイニングが完了すると、次のようなメッセージが表示されるはずです。

```
Contract mined! address: 0xdaa24d02bad7e9d6a80106db164bad9399a0423e
```

コントラクトが正常に展開できたかどうかを確認するには、次のコードを実行します。

```javascript
eth.getCode(greeter.address);
```

`0x` 以外の値を返せば成功です！

## 実行

挨拶してみます。チェーンに変更を加えないので Gas コストなしで実行できます。

```javascript
greeter.greet();
```

コントラクト作成時に予め決めたメッセージが表示されるはずです。

```javascript
"Hello World!"
```

同じコントラクトを再度実行するには、`Address` と `ABI` が必要になります。次のようにすることで、同じコントラクトの JavaScript オブジェクトをインスタンス化できます。

```javascript
var greeter2 = eth.contract(greeter.abi).at(greeter.address);
```

## コントラクトを破棄

将来的にはスケーラビリティを高めるためにブロックチェーンのレンタル機能が実装されるかもしれないとのことですが、現時点では、不要になったコントラクトは、ブロックチェーン上に放棄されます。

次のコードを実行すると、ブロックチェーンに加えられた変更に対して支払う手数料が発生します。ただし、自己破壊はネットワークによって助成されるので、通常の取引よりもはるかに安くなります。

```javascript
greeter.kill.sendTransaction({from: eth.accounts[0]});
```

`Greeter.sol` で定義した通り、所有者 (from: owner) の呼び出しに限定しているため、それ以外のアドレスからは実行できません。次のコードを実行して `0x` を返せば破棄が完了しています。

```javascript
eth.getCode(greeter.address);
```

## おわりに

基本的にチュートリアル通りの内容ですが、最新バージョンで廃止になっているコードを置き換えたり、コンパイルが通らない箇所など、部分的に書き換えているところがあります。

この記事について、何か気になるところがあれば、お気軽にご連絡ください！
