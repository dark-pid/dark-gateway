# dark-gateway

dARK Web3 Core Lib

## How to use

We created a [notebook](./docs/example_notebooks/basic_dark_usage.ipynb) to ilustrate how to use the dark-gateway lib


## Main components

### DarkGateway

The DarkGateway class is a Python class that provides a simple interface to interact with the dARK blockchain. The class is initialized with the name of the blockchain network and the configuration file. The configuration file specifies the URL of the blockchain node, the chain ID, and the minimum gas price.

Once the class is initialized, you can use it to send transactions, query the blockchain state, and interact with smart contracts. To send a transaction, you need to specify the smart contract, the method to call, and the arguments to pass to the method. The class will then sign the transaction and send it to the blockchain.

To query the blockchain state, you can use the get_balance method to get the balance of an address, or the get_transaction_receipt method to get the receipt of a transaction.

To interact with smart contracts, you can use the call method to call a function on a smart contract, or the transact method to send a transaction to a smart contract.

The DarkGateway class is a powerful tool that can be used to interact with the Darkweb blockchain. It provides a simple and easy-to-use interface that makes it easy to send transactions, query the blockchain state, and interact with smart contracts.

Here are some of the specific things that the DarkGateway class can do:

- Send transactions
- Query the blockchain state
- Interact with smart contracts
- Get the balance of an address
- Get the receipt of a transaction
- Call a function on a smart contract
- Send a transaction to a smart contract


### DarkMap
A Python class that provides a simple interface to interact with the Darkweb blockchain. It inherits from the `DarkGateway` class and adds some additional methods for interacting with the blockchain.

#### Methods

The `DarkMap` class has two main types of methods:

* **Sync methods:** These methods block until the operation is complete.
* **Async methods:** These methods return a future object that can be used to get the result of the operation.

The `DarkMap` class also has some utility methods for converting between different types of identifiers, such as the hash value of a PID and its ARK identifier.

### Examples

```python
>>> from darkmap import DarkMap
>>> darkmap = DarkMap(dark_gateway)
>>> darkmap.request_pid_hash()
'0x1234567890abcdef'
>>> darkmap.get_pid_by_hash('0x1234567890abcdef')
```


### Differences from DarkGateway

The main difference between the `DarkMap` class and the `DarkGateway` class is that the `DarkMap` class provides some additional methods for interacting with the blockchain, such as the ability to request a PID and convert between different types of identifiers.

Here is a table that summarizes the differences between the two classes:

| Feature | DarkGateway | DarkMap |
|---|---|---|
| Can send transactions | Yes | Yes |
| Can query the blockchain state | Yes | Yes |
| Can interact with smart contracts | Yes | Yes |
| Can request a PID | No | Yes |
| Can convert between different types of identifiers | No | Yes |