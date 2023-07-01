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
        

        # w3dark config parameter
        self.__blockchain_net_name = blockchain_net_name
        self.__blockchain_config = blockchain_config # could be removed

        # blockchain exec params
        self.__chain_id = int(blockchain_config['chain_id'])
        self.__min_gas_price = int(blockchain_config['min_gas_price'])
        self.__pk = blockchain_config['account_priv_key'] #FIXME: Possible security risk
        
        # important variables
        self.w3 =  self.__class__.load_blockchain_driver(blockchain_net_name,blockchain_config)
        self.deployed_contracts_dict = None

        

        # account
        self.account = self.w3.eth.account.privateKeyToAccount(self.__pk)

  
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
        
    
    def get_exec_parameters(self):
        """
            Return the blockchain execution parameters
            - chain_id
            - ming_gas_price
            - pk
        """
        return self.__chain_id,self.__min_gas_price,self.__pk


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

