#!/usr/bin/env sh
geth --datadir datadir/ init genesis.json;
cp ../keystore/keyfile datadir/keystore;
