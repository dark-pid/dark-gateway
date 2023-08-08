from web3 import Web3
from hexbytes.main import HexBytes

from .gateway import DarkGateway




class DarkDecoder:

    def __init__(self, dark_gateway: DarkGateway):
        assert type(dark_gateway) == DarkGateway, "dark_gateway must be a DarkGateway object"
        self.dgw = dark_gateway

        # populate the decode dict
        decode_dict = {}
        for key in self.dgw.deployed_contracts_dict:
            c = self.dgw.deployed_contracts_dict[key]
            decode_dict[c.address] = {'contract_name': key.split('.')[0], 'contract_object': c}
        
        self.contracts_decode_dict = decode_dict

    def extract_dark_data(self,tx_addr:[HexBytes,str]):
        """
        Extracts the parameters of a dARK method invocation from a transaction hash (addres).

        Args:
            tx_addr (str): The transaction address.

        Returns:
            dict: A dictionary that contains the following information:

                * **tx_status** (str): The status of the transaction (executed or reverted).
                * **contract_name** (str): The name of the contract that was called.
                * **function** (str): The name of the function that was called.
                * **input_parameters** (dict): The parameters that were passed to the function.
                * **logs** (list): A list of dictionaries that contain the information about the events that were emitted by the contract.
            
                **Logs** detail:
                    * **contract_name** (str): The name of the contract that emitted the event.
                    * **event_name** (str): The name of the event that was emitted.
                    * **topics** (list): A list of hexadecimal strings that represent the topics of the event.
                    * **data** (str): The data that was emitted with the event.
        
        Raises:
            TypeError: If the tx_addr argument is not a HexBytes object.
        """

        # retorno contrato, funcao , parametros da uncao, status , logs
        if type(tx_addr) == HexBytes:
            _tx_addr = tx_addr
        else:
            # raise TypeError
            _tx_addr = HexBytes(Web3.toHex(tx_addr))


        _tx = self.dgw.w3.eth.get_transaction(_tx_addr)
        try:
            _cname = self.contracts_decode_dict[_tx['to']]['contract_name']
            _cobj = self.contracts_decode_dict[_tx['to']]['contract_object']
        except KeyError:
            return None
        
        c_input = _tx['input']
        cabi = _cobj.abi

        dark_service = self.dgw.deployed_contracts_dict[_cname+'.sol']
        func_obj,func_params = dark_service.decode_function_input(c_input)

        #converting func_params
        f_params = {}

        for i in func_params.keys():
            if type(func_params[i]) == bytes:
                f_payload = Web3.toHex(func_params[i])
            else:
                f_payload = func_params[i]
            f_params[i] = f_payload

        # recibo da transacao
        r_tx = self.dgw.w3.eth.get_transaction_receipt(_tx_addr)

        if r_tx['status'] != 1: # transacao falha 0-> falha; 1-> ok; 2->falha
            logs = []
        #     return _cname, func_obj, func_params, False , []
        else:
            logs = self.extract_recepits(self.contracts_decode_dict,r_tx)
        
        output = {
            'tx_status' : 'executed' if r_tx['status'] == 1 else 'reverted',
            'contract_name' : _cname,
            'function' : func_obj,
            'input_parameters' : f_params,
            'logs' :  logs
        }
        return output

    
    ###
    ### BC UTIL
    ###

    @staticmethod
    def extract_recepits(dict_deployed_contracts,r_tx):
        """
        Extracts the receipts/transaction log from the blockchain transaction.

        Args:
            dict_deployed_contracts (dict): A dictionary of deployed contracts.
            r_tx (dict): The transaction receipt.

        Returns:
            list: A list of receipts.
        """

        r_logs = []
        for tx_log in r_tx['logs']:
            r_addr = tx_log['address']
            try:
                r_cname = dict_deployed_contracts[r_addr]['contract_name']

                # primeiro topic event-signature-hash 
                # (https://besu.hyperledger.org/en/stable/public-networks/concepts/events-and-logs/#event-signature-hash)
                topics = []
                for t in tx_log['topics'][1:]:
                    topics.append(t.hex())
                
                if len(topics) > 0:
                    r_logs.append({'contract_name': r_cname, 'topics' : topics} )

            except KeyError:
                pass
            
        return r_logs