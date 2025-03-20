# dark-gateway

The [dARK Python Library](https://github.com/dark-pid/dark-gateway) provides a convenient, low-level interface to interact directly with dARK smart contracts from your Python applications. This library supports various deployment scenarios, whether you are connecting to a public dARK network, a consortium network, or your own local/organizational deployment. With this library, you can:

* **Mint new ARK identifiers:** Register new resources and obtain their corresponding ARK IDs.
* **Resolve ARK identifiers:** Retrieve the metadata associated with a specific ARK ID.
* **Manage metadata:** (If supported by your dARK instance) Update or extend the metadata of existing ARK IDs.
* **Query the blockchain:** Access on-chain information, such as checking for the existence of an ARK ID, retrieving the owner of an ARK, and listing associated external PIDs.

The repository includes detailed documentation, installation instructions, and usage examples, making it the recommended approach for developers looking to build applications that require fine-grained control over dARK interactions or direct integration with blockchain logic. To connect to your instance, configure the library using your instance's `config.ini` and `deployed_contracts.ini` files, specifying the appropriate blockchain network and contract addresses.


## How to install

You can easily install the dARK Gateway library via `pip`. Run the following command in your terminal:

```bash
pip install dark-gateway==0.1.6
```


## How to use

We have created a [notebook](./docs/example_notebooks/basic_dark_usage.ipynb) to illustrate how to utilize the dARK Gateway library effectively. This notebook demonstrates the core functions of the library, providing practical examples for you to follow.

For more in-depth information and technical details, please refer to our comprehensive [technical documentation](docs/technical_overview.md). The intention is to enable developers to easily use this library to create new applications for dARK, fostering innovation and simplifying development processes.


