#!/usr/bin/env python3
from common import tx_args, getFromJsonOrEnv, decryptKeyFromKeyfile
from os.path import getmtime, join, exists, abspath
from web3 import Web3, HTTPProvider
from account import Account
from os import getenv
import json
import sys

deploy_node = getFromJsonOrEnv("networks.json", "DEPLOYNODE")
web3 = Web3(HTTPProvider(deploy_node))
proxy_address = web3.toChecksumAddress(getFromJsonOrEnv("addresses.json", "PROXY"))

with open("deploy_config.json") as deploy_config:
  deploy_config = json.load(deploy_config)

with open(getenv("KEYFILE")) as keyfile_c:
  keyfile = json.load(keyfile_c)

decrypt_pass = getenv("DECRYPTPASS")

deployer_decrypted_key = web3.eth.account.decrypt(keyfile, decrypt_pass)
deployer = Account(web3, deploy_config["build_path"], web3.toChecksumAddress(keyfile["address"]), deployer_decrypted_key)

proxy = deployer.instantiate_contract("Proxy", proxy_address)

WonderERC20_code_hash, WonderERC20_code = deployer.deploy("WonderfulERC20", tx_args(gas = 3000000, gasPrice = deploy_config["gas_price"]))
assert web3.eth.waitForTransactionReceipt(WonderERC20_code_hash).status == 1, "Error deploying WonderERC20 code."

upgrade_data = proxy.functions.upgradeTo(WonderERC20_code.address).buildTransaction(tx_args(gas = 3000000, gasPrice = deploy_config["gas_price"]))
upgrade_hash = deployer.send_transaction(upgrade_data)
print(f'Upgrading... {upgrade_hash}, new implementation is at address {proxy.address}')
assert web3.eth.waitForTransactionReceipt(upgrade_hash).status == 1, "Error deploying ERC20 code."
print("Upgrade succesful!")

with open("addresses.json", "w") as dump_file:
  data = {
    "PROXY":proxy.address,
    "ERC20": WonderERC20_code.address,
  }
  json.dump(data, dump_file, indent=4)
