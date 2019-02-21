#!/usr/bin/env sh
geth --datadir . --rpc --rpcport 8545 --rpcaddr 0.0.0.0 --rpccorsdomain "*" --rpcvhosts=* --nodiscover --networkid 104 --etherbase a1aa59f3980144daebd2252c709c997c880bc324 --gasprice 0 --targetgaslimit 2100000000 --gcmode archive --vmdebug console
