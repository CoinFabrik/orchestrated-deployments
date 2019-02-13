import glob
import os
import json
import sys
import rlp
from eth_utils import keccak, to_checksum_address

class Deployer:

  def __init__(self, web3, build_path):
    self.web3 = web3
    self.build_path = build_path

  def instantiate_contract(self, contract_name, contract_address):
    contract_abi, contract_bytecode = self.get_abi_and_bytecode(self.build_path, contract_name)
    contract = self.web3.eth.contract(address=contract_address, abi=contract_abi, bytecode=contract_bytecode)
    return contract

  def deploy(self, contract_name, tx_args, *constructor_args):
    sender_address = tx_args["from"]
    sender_nonce = self.web3.eth.getTransactionCount(sender_address)
    contract_address = self.generate_contract_address(sender_address, sender_nonce)
    contract = self.instantiate_contract(contract_name, contract_address)
    tx_hash = contract.constructor(*constructor_args).transact(transaction=tx_args)
    return self.web3.toHex(tx_hash), contract
  
  @staticmethod
  def get_abi_and_bytecode(build_path, contract_name):
    with open(os.path.join(build_path, contract_name + ".abi")) as contract_abi_file:
      contract_abi = json.load(contract_abi_file)
    with open(os.path.join(build_path, contract_name + ".bin")) as contract_bin_file:
      contract_bytecode = '0x' + contract_bin_file.read()
    return contract_abi, contract_bytecode

  @staticmethod
  def generate_contract_address(address, nonce):
    return to_checksum_address('0x' + keccak(rlp.encode([bytes(bytearray.fromhex(address[2:])), nonce]))[-20:].hex())