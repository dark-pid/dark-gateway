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


class DarkGateway:

    def __init__(self, blockchain_net_name: str,
                 blockchain_config: configparser.SectionProxy):
        
        #TODO: MODIFY CONSTRUCTOR PARAMATERS
        assert type(blockchain_net_name) == str, "blockchain_net_name must be str type"
        assert type(blockchain_config) == configparser.SectionProxy, "blockchain_config must be configparser.SectionProxy type"
        

        ### w3dark config parameter
        self.__blockchain_net_name = blockchain_net_name
        self.__blockchain_config = blockchain_config # could be removed

        ### blockchain exec params
        self.__chain_id = int(blockchain_config['chain_id'])
        self.__min_gas_price = int(blockchain_config['min_gas_price'])
        self.__pk = blockchain_config['account_priv_key'] #FIXME: Possible security risk
        self.min_gas_price = '100' #FIXME: add configuration parameter

        ### important variables
        self.w3 =  self.__class__.load_blockchain_driver(blockchain_net_name,blockchain_config)
        self.deployed_contracts_dict = None

        ### account
        self.__account = self.w3.eth.account.privateKeyToAccount(self.__pk)
        # endereco da autoridade
        #TODO: modelar utilizar  multiplas autoridades
        #TODO: colocar como variavel de configuração
        #FIXME: quando for necessario utilizar multiplas autoridades
        self.authority_addr = "0xf17f52151EbEF6C7334FAD080c5704D77216b732"
  
    def load_deployed_smart_contracts(self,deployed_contracts_config:configparser.ConfigParser):
        """
            Load the deployed smart contracts
            - Ity is essential notice that it is important to configure the smart contract
        """
        assert type(deployed_contracts_config) == configparser.ConfigParser, "deployed_contracts_config must be configparser.ConfigParser type"
        # self.__deployed_contracts_config = deployed_contracts_config

        contracts_dict = {}
        for k in list(deployed_contracts_config.keys()):
            if k != 'DEFAULT':
                addr = deployed_contracts_config[k]['addr']
                c_abi = ast.literal_eval(deployed_contracts_config[k]['abi'])['abi']
                contracts_dict[k] = self.w3.eth.contract(address=addr, abi=c_abi)

        # TODO: CHECK IF CONTRANCT DICT ARE EMPTY
        self.deployed_contracts_dict = contracts_dict
        
    def is_deployed_contract_loaded(self):
        return self.deployed_contracts_dict != None
    
    def get_exec_parameters(self):
        """
            Return the blockchain execution parameters
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
        #get the gas needed
        est_gas = smart_contract.get_function_by_name(method)(*args).estimateGas()
        print("-----")
        print(est_gas)
        print("-----")
        tx_params = self.get_tx_params(est_gas)
        #build the transaction
        tx = smart_contract.get_function_by_name(method)(*args).buildTransaction(tx_params)
        signed_tx = self.__account.signTransaction(tx)
        return signed_tx
    



    ###
    ### private methods
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
        elif 'dpi-' in blockchain_net_name:
            # blockchain_config = config[blockchain_net_name]
            # blockchain_config['url']
            w3 = Web3(Web3.HTTPProvider(blockchain_config['url']))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            # return w3
        else:
            raise RuntimeError('This shouldnt happend :: Not implemented')
        
        return w3

