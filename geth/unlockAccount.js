
function unlock() {
 for (var j = 0; j < eth.accounts.length; j++) {
    personal.unlockAccount(eth.accounts[j], "coinfabrik123", 22000);
  }
}
unlock();

miner.start(1);
