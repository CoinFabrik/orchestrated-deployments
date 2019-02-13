from eth_utils import keccak, to_checksum_address
import rlp
import json
import os

class Account:

  def __init__(self, web3, build_path, address, decrypted_key):
    self.web3 = web3
    self.build_path = build_path
    self.address = address
    self.decrypted_key = decrypted_key
    self.nonce = web3.eth.getTransactionCount(address)

  def instantiate_contract(self, contract_name, contract_address):
    contract_abi, contract_bytecode = self.get_abi_and_bytecode(self.build_path, contract_name)
    contract = self.web3.eth.contract(address=contract_address, abi=contract_abi, bytecode=contract_bytecode)
    return contract

  def deploy(self, contract_name, tx_args, *constructor_args):
    print("\nDeploying contract: {}".format(contract_name))
    contract_address = self.generate_contract_address(self.address, self.nonce)
    tx_args["nonce"] = self.nonce
    self.nonce += 1
    contract = self.instantiate_contract(contract_name, contract_address)
    tx_data = contract.constructor(*constructor_args).buildTransaction(tx_args)
    signed_tx = self.web3.eth.account.signTransaction(tx_data, self.decrypted_key)
    tx_hash = self.web3.toHex(self.web3.eth.sendRawTransaction(signed_tx.rawTransaction))
    print("Contract {0} deployment transaction hash: {1}\n".format(contract_name, tx_hash))
    return tx_hash, contract

  @staticmethod
  def generate_contract_address(address, nonce):
    return to_checksum_address('0x' + keccak(rlp.encode([bytes(bytearray.fromhex(address[2:])), nonce]))[-20:].hex())

  @staticmethod
  def get_abi_and_bytecode(compiled_path, contract_name):
    absolpath = os.path.join(compiled_path, contract_name)
    with open(absolpath + ".abi") as contract_abi_file:
      contract_abi = json.load(contract_abi_file)
    with open(absolpath + ".bin") as contract_bin_file:
      contract_bytecode = '0x' + contract_bin_file.read()
    return contract_abi, contract_bytecode