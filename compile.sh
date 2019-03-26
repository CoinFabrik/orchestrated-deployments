#!/usr/bin/env sh
cd contracts
./../solc-5.6 --abi --bin --overwrite --optimize --optimize-runs 0 -o ../build Proxy.sol
./../solc-5.6 --abi --bin --overwrite --optimize --optimize-runs 0 -o ../build ERC20.sol
./../solc-5.6 --abi --bin --overwrite --optimize --optimize-runs 0 -o ../build WonderfulERC20.sol
