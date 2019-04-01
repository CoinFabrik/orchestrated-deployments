#!/usr/bin/env python3

from decrypt import decryptKeyFromKeyfile
from os.path import getmtime, join, exists, abspath
from web3 import Web3, HTTPProvider
from tx_args import tx_args
from account import Account
from os import getenv
import json
import sys

try:
  with open("addresses.json") as address_file:
    addresses = json.load(address_file)
    proxy_address = addresses["PROXY"]
    print("Reaching proxy address from addresses.json file.")
except FileNotFoundError as err:
  proxy_address = getenv("PROXYADDRESS") if getenv("PROXYADDRESS") is not None else raise("Can't reach proxy address.")
  print("Reaching proxy address from environment.")

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

proxy = deployer.instantiate_contract("Proxy", addresses["proxy"])

WonderERC20_code_hash, WonderERC20_code = deployer.deploy("WonderfulERC20", tx_args(gas = 3000000, gasPrice = deploy_config.gasPrice=))
assert web3.eth.waitForTransactionReceipt(WonderERC20_code_hash).status == 1, "Error deploying WonderERC20 code."

upgrade_data = proxy.functions.upgradeTo(WonderERC20_code.address).buildTransaction(tx_args())
upgrade_hash = deployer.send_transaction(upgrade_data)
print(f'Upgrading... {upgrade_hash}, new implementation is at address {proxy.address}')
assert web3.eth.waitForTransactionReceipt(upgrade_hash).status == 1, "Error deploying ERC20 code."
print("Upgrade succesful!")

with open("addresses.json", "w") as dump_file:
  data = {
    "PROXY":proxy.address,
    "ERC20": ERC20_code.address,
  }
  json.dump(data, dump_file, indent=4)
