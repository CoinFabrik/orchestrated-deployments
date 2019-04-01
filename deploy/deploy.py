#!/usr/bin/env python3
from decrypt import decryptKeyFromKeyfile
from os.path import getmtime, join, exists, abspath
from web3 import Web3, HTTPProvider
from account import Account
from getpass import getpass
from tx_args import tx_args
import argparse
import sys
import json

try:
  with open("networks.json") as networks_file:
    networks = json.load(networks_file)
    main_node = networks["MAINNODE"]
  print("Reaching main node URL from networks.json file")
except FileNotFoundError as err:
  main_node = getenv("MAINNODE") if getenv("MAINNODE") is not None else raise("Can't reach main node URL.")
  print("Reaching main node URL from environment.")  

with open("deploy_config.json") as deploy_config:
  deploy_config = json.load(deploy_config)

web3 = Web3(HTTPProvider(main_node))

deployer_address, deployer_decrypted_key = decryptKeyFromKeyfile(deploy_config.keyfile_path, getpass("Insert decryption password:"))
deployer = Account(web3, deploy_config.build_path, deployer_address, deployer_decrypted_key)

ERC20_code_hash, ERC20_code = deployer.deploy("ERC20", tx_args(gas = 3000000, gasPrice = deploy_config.gas_price))
assert web3.eth.waitForTransactionReceipt(ERC20_code_hash).status == 1, "Error deploying ERC20 code."
print("Transaction sucessfull... contract at {}".format(ERC20_code.address))

proxy_hash, proxy = deployer.deploy("Proxy", tx_args(gas = 3000000, gasPrice = deploy_config.gas_price), ERC20_code.address, "0x")
assert web3.eth.waitForTransactionReceipt(proxy_hash).status == 1, "Error deploying ERC20 code."
print("Transaction sucessfull... contract at {}".format(proxy.address))

with open("addresses.json", "w") as dump_file:
  data = {
    "PROXY":proxy.address,
    "ERC20": ERC20_code.address,
  }
  json.dump(data, dump_file, indent=4)
