#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   setup.py
@Time    :   2022/05/13 10:20:06
@Author  :   Thiago Nóbrega 
@Contact :   thiagonobrega@gmail.com
'''

import os
import logging
import ast
import configparser

from web3 import Web3, IPCProvider
from web3.middleware import geth_poa_middleware

# from eth_tester import PyEVMBackend
from web3.providers.eth_tester import EthereumTesterProvider
from web3.exceptions import TransactionNotFound


class DarkGateway:

    def __init__(self, blockchain_config: configparser.SectionProxy, deployed_contracts_config=None):
        """
        Constructor.

        Args:
            blockchain_config (configparser.SectionProxy): The blockchain configuration.
            deployed_contracts_config (configparser.SectionProxy): Deployed contracts configuration.
        """

        #TODO: MODIFY CONSTRUCTOR PARAMATERS
        assert type(blockchain_config) == configparser.ConfigParser, "blockchain_config must be configparser.ConfigParser type"
        if deployed_contracts_config!=None:
            assert type(blockchain_config) == configparser.ConfigParser, "blockchain_config must be configparser.ConfigParser type"
        

        ### w3dark config parameter
        self.__blockchain_net_name = blockchain_config['base']['blockchain_net']
        self.__blockchain_net_config = blockchain_config[self.__blockchain_net_name] # could be removed
        self.__blockchain_base_config = blockchain_config['base']
        self.__blockchain_smartcontracts_config = blockchain_config['smartcontracts']

        ### blockchain exec params
        self.__chain_id = int(self.__blockchain_net_config['chain_id'])
        self.__min_gas_price = int(self.__blockchain_net_config['min_gas_price'])
        self.__pk = self.__blockchain_net_config['account_priv_key'] #FIXME: Possible security risk
        self.min_gas_price = str(self.__blockchain_net_config['min_gas_price']) 

        ### important variables
        self.w3 =  self.__class__.load_blockchain_driver(self.__blockchain_net_name,self.__blockchain_net_config)

        #load smartcontracts
        if deployed_contracts_config!=None:
            self.deployed_contracts_dict = self.__class__.__load_deployed_smart_contracts(self.w3,deployed_contracts_config)
        else:
            self.deployed_contracts_dict = None

        ### account
        self.__account = self.w3.eth.account.privateKeyToAccount(self.__pk)
        # endereco da autoridade
        #TODO: modelar utilizar  multiplas autoridades
        #FIXME: quando for necessario utilizar multiplas autoridades
        self.authority_addr = self.__account.address #self.__blockchain_base_config['authority_addr']
        

    def is_deployed_contract_loaded(self):
        return self.deployed_contracts_dict != None
    
    def get_blockchain_net_config(self):
        return self.__blockchain_net_config
    
    def get_blockchain_base_config(self):
        return self.__blockchain_base_config
    
    def get_blockchain_smartcontracts_config(self):
        return self.__blockchain_smartcontracts_config
    
    def get_exec_parameters(self):
        """
        Return the blockchain execution parameters.

        Returns:
            tuple: The blockchain execution parameters.
            - chain_id
            - ming_gas_price
            - pk
        """
        return self.__chain_id,self.__min_gas_price,self.__pk
    
    ####
    #### sing and send parameters
    ####

    def get_tx_params(self,gas):
        """
        Method employed to retrive the BC tx params

        Args:
            gas (int): The gas limit for the transaction.

        Returns:
            dict: The transaction parameters.
        """
                    #   w3,gas,account,chain_id=1337,min_gas_price='100'):
        # nonce = w3.eth.getTransactionCount(acount.address)
        nonce = self.w3.eth.getTransactionCount(self.w3.toChecksumAddress(self.__account.address))
        tx_params = {'from': self.__account.address,
                    # 'to': contractAddress,
                    'nonce': nonce,
                    'gas': gas * 2,
                    'gasPrice': self.w3.toWei(self.min_gas_price, 'gwei'), # defaul min gas price to besu (nao funciona w3.eth.gas_price)
                    'chainId': self.__chain_id
        }
        return tx_params
    
    def signTransaction(self,smart_contract,method,*args):
        """
        Sign a transaction with the specified smart contract and method.

        Args:
            smart_contract (Contract): The smart contract to interact with.
            method (str): The name of the method to call.
            args (tuple): The arguments to pass to the method.

        Returns:
            Transaction: The signed transaction.
        """
        #get the gas needed
        est_gas = smart_contract.get_function_by_name(method)(*args).estimateGas()
        tx_params = self.get_tx_params(est_gas)
        #build the transaction
        tx = smart_contract.get_function_by_name(method)(*args).buildTransaction(tx_params)
        signed_tx = self.__account.signTransaction(tx)
        return signed_tx
    
    ####
    #### transaction status
    ####

    def transaction_was_executed(self,tx_hash):
        """
        This function checks if a transaction was executed.

        Args:
            tx_hash (str/Hexbyte): The hash of the transaction to check.

        Returns:
            bool, TransactionReceipt: A tuple of whether the transaction was executed and the transaction receipt, if it was executed.

        Raises:
            TransactionNotFound: If the transaction was not found.
        """
        try:
            tx_recipt = self.w3.eth.getTransactionReceipt(tx_hash)
        except TransactionNotFound:
            return False , None
        return True , tx_recipt

    
    ###
    ### deploy contracts
    ###
    def deploy_contract_besu(self,contract_interface):
   
        sc = self.w3.eth.contract( abi=contract_interface['abi'],
                                bytecode=contract_interface['bin']
                                )

        est_gas = sc.constructor().estimateGas()
        tx_const = sc.constructor().buildTransaction(self.get_tx_params(est_gas))
        signed_tx = self.__account.signTransaction(tx_const)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        tx_receipt = None
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        return tx_receipt['contractAddress']
    
    ###
    ### private methods
    ###

    def get_blockchain_config(self):
        return self.__blockchain_net_config
    
    def get_account_balance(self):
        return Web3.fromWei(self.w3.eth.get_balance(self.__account.address),'ether')

    ###
    ### static methods
    ###
    @staticmethod
    def load_blockchain_driver(blockchain_net_name: str,blockchain_config: configparser.SectionProxy) -> Web3:
        """
            Load the blockchain driver.

            The drive is used to connect the application to the blockchain.
            The configuration is defined in config.ini file.
        """
        assert type(blockchain_net_name) == str, "blockchain_net_name must be str type"
        assert type(blockchain_config) == configparser.SectionProxy, "blockchain_config must be configparser.SectionProxy type"
        
        #debug
        # logging.info(config_file)
        w3 = None

        if blockchain_net_name == 'EthereumTesterPyEvm':
            raise(Exception("Not Suported"))
            # return Web3(EthereumTesterProvider(PyEVMBackend()))
        elif 'dark-' in blockchain_net_name:
            # blockchain_config = config[blockchain_net_name]
            # blockchain_config['url']
            w3 = Web3(Web3.HTTPProvider(blockchain_config['url']))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # return w3
        else:
            raise RuntimeError('This shouldnt happend :: Not implemented')
        
        return w3
    
    @staticmethod
    def __load_deployed_smart_contracts(w3,deployed_contracts_config:configparser.ConfigParser):
        """
            Load the deployed smart contracts
            - Ity is essential notice that it is important to configure the smart contract

            Args:
                deployed_contracts_config (configparser.ConfigParser): The deployed smart contracts configuration.
        """
        assert type(deployed_contracts_config) == configparser.ConfigParser, "deployed_contracts_config must be configparser.ConfigParser type"
        # self.__deployed_contracts_config = deployed_contracts_config

        contracts_dict = {}
        for k in list(deployed_contracts_config.keys()):
            if k != 'DEFAULT':
                addr = deployed_contracts_config[k]['addr']
                c_abi = ast.literal_eval(deployed_contracts_config[k]['abi'])#['abi']
                contracts_dict[k] = w3.eth.contract(address=addr, abi=c_abi)

        # TODO: CHECK IF CONTRANCT DICT ARE EMPTY
        if len(contracts_dict.keys()) == 0:
            return None
        
        return contracts_dict
