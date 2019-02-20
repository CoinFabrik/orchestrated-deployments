#!/usr/bin/env python3

from web3 import Web3, HTTPProvider
import json
import argparse
from account import Account
import sys
from os.path import getmtime, join, exists, abspath

def parse_args(args):
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--network", default="http://localhost:8545", help="Enter network, defaults to localhost:8545")
  parser.add_argument("-a", "--address", help="Enter the new implementation address")
  return parser.parse_known_args(args)

def tx_args(gas=200000, gasPrice=3000000000, value=0, nonce=None):
  args = {"value": Web3.toWei(value, "ether"), "gas": gas, "gasPrice": gasPrice or 2000000000}
  if nonce is not None:
    args["nonce"] = nonce
  return args

args, unknown = parse_args(sys.argv[1: ])

web3 = Web3(HTTPProvider(args.network))

build_path = "build"

with open("keystore/test") as key_file:
  file_content = json.load(key_file)
  deployer_address = web3.toChecksumAddress(file_content["address"])
  deployer_encrypted_key = file_content
  deployer_decryption_key = "test"
  deployer_decrypted_key = web3.eth.account.decrypt(deployer_encrypted_key, deployer_decryption_key)

with open("addresses.json") as address_file:
  addresses = json.load(address_file)

deployer = Account(web3, build_path, deployer_address, deployer_decrypted_key)
proxy = deployer.instantiate_contract("Proxy", addresses["proxy"])

WonderERC20_code_hash, WonderERC20_code = deployer.deploy("WonderfulERC20", tx_args(gas = 3000000, gasPrice = gas_price))
assert web3.eth.waitForTransactionReceipt(WonderERC20_code_hash).status == 1, "Error deploying WonderERC20 code."

upgrade_data = proxy.functions.upgradeTo(addresses["WonderfulERC20"]).buildTransaction(tx_args())
upgrade_hash = deployer.send_transaction(upgrade_data)
print(f'Upgrading... {upgrade_hash}')
assert web3.eth.waitForTransactionReceipt(upgrade_hash).status == 1, "Error deploying ERC20 code."
print("Upgrade succesful!")