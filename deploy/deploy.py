#!/usr/bin/env python3
from common import tx_args, getFromJsonOrEnv, decryptKeyFromKeyfile
from os.path import getmtime, join, exists, abspath
from web3 import Web3, HTTPProvider
from account import Account
from os import getenv
import argparse
import sys
import json

with open("deploy_config.json") as deploy_config:
  deploy_config = json.load(deploy_config)

deploy_node = getFromJsonOrEnv("networks.json", "DEPLOYNODE")
web3 = Web3(HTTPProvider(deploy_node))

with open(getenv("KEYFILE")) as keyfile_c:
  keyfile = json.load(keyfile_c)

decrypt_pass = getenv("DECRYPTPASS")


deployer_address, deployer_decrypted_key = decryptKeyFromKeyfile(web3, keyfile, decrypt_pass)
deployer = Account(web3, deploy_config["build_path"], deployer_address, deployer_decrypted_key)

ERC20_code_hash, ERC20_code = deployer.deploy("ERC20", tx_args(gas = 3000000, gasPrice = deploy_config["gas_price"]))
assert web3.eth.waitForTransactionReceipt(ERC20_code_hash).status == 1, "Error deploying ERC20 code."
print("Transaction sucessfull... contract at {}".format(ERC20_code.address))

proxy_hash, proxy = deployer.deploy("Proxy", tx_args(gas = 3000000, gasPrice = deploy_config["gas_price"]), ERC20_code.address, "0x")
assert web3.eth.waitForTransactionReceipt(proxy_hash).status == 1, "Error deploying ERC20 code."
print("Transaction sucessfull... contract at {}".format(proxy.address))

with open("addresses.json", "w") as dump_file:
  data = {
    "PROXY":proxy.address,
    "ERC20": ERC20_code.address,
  }
  json.dump(data, dump_file, indent=4)
