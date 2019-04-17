#!/usr/bin/env python3
from common import tx_args, getFromJsonOrEnv, decryptKeyFromKeyfile
from os.path import getmtime, join, exists, abspath
from web3 import Web3, HTTPProvider
from account import Account
from os import getenv
import json
import sys

proxy_address = getFromJsonOrEnv("addresses.json", "PROXY")
test_node = getFromJsonOrEnv("networks.json", "TESTNODE")

with open("deploy_config.json") as deploy_config:
  deploy_config = json.load(deploy_config)

web3 = Web3(HTTPProvider(test_node))

with open(getenv("KEYFILE")) as keyfile_c:
  keyfile = json.load(keyfile_c)

decrypt_pass = getenv("DECRYPTPASS")

deployer_address, deployer_decrypted_key = decryptKeyFromKeyfile(web3, keyfile, decrypt_pass)
deployer = Account(web3, deploy_config["build_path"], deployer_address, deployer_decrypted_key)

wonder_erc20 = deployer.instantiate_contract("WonderfulERC20", proxy_address)

try:
  print("Calling function getMessage()")
  print(f"Received: {wonder_erc20.functions.getWonderfulMessage().call()}")
except Exception as err:
  print(f"Received an error {err}")
