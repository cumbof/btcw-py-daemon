# btcw-py-daemon

This is a simple python script that exploits the pybitcoin library to generate public and private keys and make a query to blockchain.info to chaeck if the generated address is in use, retrieving also its balance.

If an address with a positive balance would be discovered, its private key will be stored in a local database defined by the schema.sql file.

This script is intended for testing purposes only. It is practically impossible that it would generate a btc address already in use.

### Requirements
- Python 2.7
- [pybitcoin](https://github.com/blockstack/pybitcoin)
