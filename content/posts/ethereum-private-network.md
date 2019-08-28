+++
date = "2018-06-20T22:15:00+09:00"
draft = false
title = "Ethereum Private Network"
tags = ["Ethereum", "Blockchain"]
image = "/images/headers/ethereum.png"
+++

スマートコントラクト (DApps) の開発を行うために、イーサリアムの公式 CLI である [Geth](https://github.com/ethereum/go-ethereum) を使用して、プライベートネットワークを構築していきます。

## 開発環境のディレクトリ構成

このような環境を構築します。

```bash
tree -a
.
├── .ethereum-dev
│   ├── clients
│   │   └── 1
│   └── miner
└── genesis.json
```

マイナーとその他のクライアントで分ける理由ですが、 geth コンソール上で開発とマイニングを同時に行うと Ether の送金やコントラクト実行のために消費される Gas コストなどが、同時に得られるマイニング報酬とごっちゃになり、確認しずらくなってしまうのを避けるためです。

## ネットワーク ID を定義

プライベートネットワークの ID を決めます。既知の値は避けてください。

```bash
NETID=15
```

## Genesis ブロックを定義

始祖となるブロックを定義します。

```bash
cat <<EOF> genesis.json
{
  "config": {
    "chainId": $NETID
  },
  "nonce": "0x0000000000000042",
  "timestamp": "0x0",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "extraData": "",
  "gasLimit": "0x8000000",
  "difficulty": "0x4000",
  "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "coinbase": "0x3333333333333333333333333333333333333333",
  "alloc": {}
}
EOF
```

## Geth を用意

macOS の場合は、公式ウォレットの [Mist](https://github.com/ethereum/mist) に含まれる Geth を使います。

```bash
geth() { $HOME/Library/Application\ Support/Ethereum\ Wallet/binaries/Geth/unpacked/geth $*; }
```

## マイナーを初期化

データディレクトリを決めます。

```bash
DATA=$HOME/.ethereum-dev/miner
```

genesis.json より初期化します。

```bash
geth --datadir $DATA init genesis.json
```

## クライアントを初期化

データディレクトリを決めます。

```bash
DATA=$HOME/.ethereum-dev/clients/1
```

genesis.json より初期化します。

```bash
geth --datadir $DATA init genesis.json
```

一度起動してマイニング報酬の宛先となるアカウントを作成しておきます。

```bash
geth --datadir $DATA --networkid $NETID --port 30305 console 2>> $DATA/err.log
> 
> personal.newAccount('')  // Create an empty password account
> "0x71efd180a2246663624a3e6f13da97b9315815f3"
> exit
```

## マイニングを開始

マイニング報酬の宛先をクライアントが持つアドレス指定して実行後、ログに出力されたノード情報をコピーします。

```bash
ETHERBASE=0x71efd180a2246663624a3e6f13da97b9315815f3

geth --datadir $DATA --networkid $NETID --identity miner \
     --port 30304 --lightserv 75 --lightpeers 10 --shh \
     --mine --minerthreads 1 --etherbase $ETHERBASE \
     --ipcpath geth.ipc
...
INFO [06-21|20:56:52] UDP listener up self=enode://84a278e86445104cb2552369acf31a5e6b74751fd9e57bffcaa8e89e65d63ec30ee560ba6e1ef1c312af0f7859c875b0ce043d066d33542e29a48813b2f9ba54@[::]:30304
...
```

## クライアントを起動

マイナーのノード情報を `bootnodes` に指定して起動します。

```bash
MINERADDR=127.0.0.1

BOOTNODES=enode://84a278e86445104cb2552369acf31a5e6b74751fd9e57bffcaa8e89e65d63ec30ee560ba6e1ef1c312af0f7859c875b0ce043d066d33542e29a48813b2f9ba54@$MINERADDR:30304

geth --datadir $DATA --networkid $NETID --identity client \
     --port 30305 --bootnodes $BOOTNODES --shh \
     --rpc --rpcaddr 0.0.0.0 --rpcport 8104 \
     --ws --wsaddr 0.0.0.0 --wsport 8105 \
     --ipcpath geth.ipc \
     console 2>> $DATA/err.log
> 
> eth.blockNumber  // Check number
> web3.fromWei(eth.getBalance(eth.coinbase), 'ether');
```

もしクライアントでマイニングをする場合、コンソール上で下記のようにします。

```javascript
miner.start();

// 採掘できるまでちょっと待つ

miner.stop();
```

## おわりに

今回作成したネットワークは、 MetaMask を介して接続することも可能です。

この記事について、何か気になるところがあれば、チャットや SNS などでお気軽にご連絡ください。
