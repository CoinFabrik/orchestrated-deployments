def tx_args(gas=200000, gasPrice=3000000000, value=0, nonce=None):
  args = {"value": Web3.toWei(value, "ether"), "gas": gas, "gasPrice": gasPrice or 2000000000}
  if nonce is not None:
    args["nonce"] = nonce
  return args