+++
date = "2018-06-20T22:15:00+09:00"
draft = false
title = "Ethereum Private Network"
tags = ["ethereum", "blockchain"]
image = "/images/headers/ethereum.png"
+++

スマートコントラクト (DApps) の開発を行うために、イーサリアムの公式 CLI である [Geth](https://github.com/ethereum/go-ethereum) を使用して、プライベートネットワークを構築していきます。

## データディレクトリを作成

```bash
mkdir $HOME/eth-dev
```

## Genesis ブロックを定義

```bash
cat <<EOF> $HOME/eth-dev/genesis.json
{
  "config": {
    "chainId": 15
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

## プライベートネットワークを初期化

macOS にインストールされた公式ウォレットの [Mist](https://github.com/ethereum/mist) に含まれる Geth を使います。

```bash
$HOME/Library/Application\ Support/Ethereum\ Wallet/binaries/Geth/unpacked/geth \
  --datadir $HOME/eth-dev \
  init $HOME/eth-dev/genesis.json
```

## ノードを起動

```bash
$HOME/Library/Application\ Support/Ethereum\ Wallet/binaries/Geth/unpacked/geth \
  --networkid 15 \
  --nodiscover \
  --datadir $HOME/eth-dev \
  --port 30403 \
  --rpc \
  console 2>> $HOME/eth-dev/err.log
> 
> personal.newAccount()         # Create an empty password account
> eth.getBalance(eth.coinbase)  # Nothing
> eth.blockNumber               # Nothing
> miner.start()                 # Wait until the block is mined
> miner.stop()
> eth.blockNumber               # Check number
> 
> web3.fromWei(eth.getBalance(eth.coinbase), 'ether')  # Checking
```

## おわりに

今回作成したネットワークは、 MetaMask を介して接続することも可能です。

この手順は、随時更新する予定ですが、何かおかしなところがあれば SNS などでお気軽にご連絡ください。
