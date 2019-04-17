from web3 import Web3
from os import getenv
web3 = Web3(Web3.HTTPProvider(getenv("DEPLOYNODE")))
web3.eth.sendTransaction({"from":web3.eth.accounts[0], "to":web3.toChecksumAddress("0xa974c8a2da66127c78b6dfc7cadebe443450da60"), "value": web3.toWei(2,"ether")})