#!/usr/bin/env sh
geth --datadir datadir/ --rpc --rpcapi eth,web3,miner --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*" --rpcvhosts=* --nodiscover --networkid 104 --etherbase 1d294de6b8536b211dc249e03dffaa10c8fc9acf --gasprice 0 --targetgaslimit 2100000000 --gcmode archive --vmdebug  --preload unlockAccount.js console
