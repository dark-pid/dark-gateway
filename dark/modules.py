from web3 import Web3
from hexbytes.main import HexBytes

from .gateway import DarkGateway
from .util import invoke_contract_sync, invoke_contract_async
from .pid_modules import DarkPid, PayloadSchema , Payload


class DarkMap:
    
    def __init__(self, dark_gateway: DarkGateway):
        assert type(dark_gateway) == DarkGateway, "dark_gateway must be a DarkGateway object"
        assert dark_gateway.is_deployed_contract_loaded() == True, "dark_gateway must be loaded with deployed contracts"

        #dark gatewar
        self.gw = dark_gateway

        ##
        ## dARK SmartContracts
        ##

        # databases for query
        self.dpid_db = dark_gateway.deployed_contracts_dict['PidDB.sol']
        self.epid_db = dark_gateway.deployed_contracts_dict['ExternalPidDB.sol']
        self.url_db = dark_gateway.deployed_contracts_dict['UrlDB.sol']
        # authorities db to configuration
        self.auth_db = dark_gateway.deployed_contracts_dict['AuthoritiesDB.sol']
        #dARK services
        self.dpid_service = dark_gateway.deployed_contracts_dict['PIDService.sol']
        self.epid_service = dark_gateway.deployed_contracts_dict['ExternalPIDService.sol']
        self.url_service = dark_gateway.deployed_contracts_dict['UrlService.sol']
        self.auth_service = dark_gateway.deployed_contracts_dict['AuthoritiesService.sol']
        #payload schema name
        self.payload_schema_name = dark_gateway.payload_schema_name
    
    ###################################################################
    ###################################################################
    #####################  INTERNAL METHODS  #########################
    ###################################################################
    ###################################################################
    
    def __request_pid_hash(self):
        signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        return signed_tx
    
    def __add_external_pid(self,hash_pid: HexBytes,external_pid: str,pid_shema:int):
        # 0 doi
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        return self.gw.signTransaction(self.dpid_service , 'addExternalPid', hash_pid, pid_shema , external_pid)
    
    def __set_url(self,hash_pid: HexBytes,ext_url: str):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        return self.gw.signTransaction(self.dpid_service , 'set_url', hash_pid, ext_url)
    
    def __set_payload(self,hash_pid: HexBytes,payload: dict):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"

        try:
            payload_schema =  self.get_payload_schema_by_name(self.payload_schema_name)
        except Exception as e:
            raise Exception("Unable to retrieve the payload schema \n \t\t {}".format(e))
        
        # valida se todos os atributos do payload estao no schema
        self.validade_payload(payload,payload_schema)

        signed_tx_set = []
        
        for p in payload.keys():      
            att_n = str(p.upper())
            att_v = str(payload[p])
            # print('{}:{}'.format(att_n,att_v))
            # print('-----------')
                        
            # signed_tx = self.gw.signTransaction(self.dpid_service , 'set_payload', hash_pid, att_n , att_v )
            signed_tx = self.gw.signTransaction(self.dpid_service , 'set_payload_tmp', hash_pid,
                                                payload_schema.schema_name, att_n , att_v )
            signed_tx_set.append(signed_tx)
        
        return signed_tx_set      
    

    ###################################################################
    ###################################################################
    ###################### SYNC METHODS ###############################
    ###################################################################
    ###################################################################

    def sync_request_pid_hash(self):
        """
            Request a PID and return the hash (address) of the PID
        """
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        signed_tx = self.__request_pid_hash()
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        dark_id = receipt['logs'][0]['topics'][1]
        return dark_id
    
    def bulk_request_pid_hash(self):
        """
            Request a PID and return the hash (address) of the PID
        """
        signed_tx = self.gw.signTransaction(self.dpid_service , 'bulk_assingID', self.gw.authority_addr)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        #retrieving pidhashs
        pid_hashes = []
        for i in range(len(receipt['logs'])):
            try :
                pid_hashes.append(receipt['logs'][i]['topics'][1])
                # b = dm.convert_pid_hash_to_ark(pid_hash)
            except IndexError:
                pass
        return pid_hashes
    
    def sync_request_pid(self):
        """
            Request a PID and return the ark of the PID
        """
        return self.convert_pid_hash_to_ark(self.sync_request_pid_hash())
    
    def sync_add_external_pid(self,hash_pid: HexBytes,external_pid: str,pid_schema=0):
        # assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'addExternalPid', hash_pid, 0 , external_pid)
        signed_tx = self.__add_external_pid(hash_pid,external_pid,pid_schema)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        return self.convert_pid_hash_to_ark(hash_pid)
    
    def sync_set_url(self,hash_pid: HexBytes,ext_url: str):
        # assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'set_url', hash_pid, ext_url)
        signed_tx = self.__set_url(hash_pid,ext_url)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        return self.convert_pid_hash_to_ark(hash_pid)
    
    def sync_set_payload(self,hash_pid: HexBytes,payload: dict):
        
        tx_set = self.__set_payload(hash_pid,payload)
        for signed_tx in tx_set:        
            receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        
        return self.convert_pid_hash_to_ark(hash_pid)
    

        
    
    ###################################################################
    ###################################################################
    ##################### ASYNC METHODS ###############################
    ###################################################################
    ###################################################################
    
    def async_request_pid_hash(self):
        """
            Request a PID and return the hash (address) of the PID
        """
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        signed_tx = self.__request_pid_hash()
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_external_pid(self,hash_pid: HexBytes,external_pid: str,pid_schema=0):
        # assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'addExternalPid', hash_pid, 0 , external_pid)
        signed_tx = self.__add_external_pid(hash_pid,external_pid,pid_schema)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_url(self,hash_pid: HexBytes,ext_url: str):
        # assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'set_url', hash_pid, ext_url)
        signed_tx = self.__set_url(hash_pid,ext_url)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_payload(self,hash_pid: HexBytes,payload: dict):
        """
        Asynchronously sets the payload of a PID.

        Args:
            hash_pid (HexBytes): The hash value of the PID.
            pay_load (dict): The payload to be set.

        Returns:
            asyncio.Future: A future object that resolves to the transaction receipt.

        Raises:
            TypeError: If the hash_pid argument is not a HexBytes object.
        """
        signed_tx_set = self.__set_payload(hash_pid,payload)
        tx_addr_set = []
        for signed_tx in signed_tx_set:        
            r_tx = invoke_contract_async(self.gw,signed_tx)
            tx_addr_set.append(r_tx)
    
        return tx_addr_set #r_tx


    ###################################################################
    ###################################################################
    #####################  UTIL METHODS  ##############################
    ###################################################################
    ###################################################################

    def convert_pid_hash_to_ark(self,dark_pid_hash):
        """
            Convert the dark_pid_hash to a ARK identifier
        """
        return self.dpid_db.caller.get(dark_pid_hash)[1]
    
    
    
    ###################################################################
    ###################################################################
    ### Onchain core queries
    ###################################################################
    ###################################################################

    def get_pid_by_hash(self,dark_id):
        """
            Retrieves a persistent identifier (PID) by its hash value.

            Parameters:
                dark_id (str): The hash value of the PID.

            Returns:
                str: The PID associated with the given hash value.

            Raises:
                AssertionError: If the dark_id does not start with '0x'.
        """
        assert dark_id.startswith('0x'), "id is not hash"
        dark_object = self.dpid_db.caller.get(dark_id)
        payload_hash = dark_object[-2]
        # b'\x00' * 32 = 0
        if payload_hash != b'\x00' * 32:
            payload_py_obj = self.get_payload(payload_hash)
        else:
            payload_py_obj = None
        
        # return DarkPid.populateDark(dark_object,self.epid_db,self.url_service)
        return DarkPid.populate(dark_object,self.epid_db,self.url_service,payload_py_obj)

    def get_pid_by_ark(self,dark_id):
        """
            Retrieves a persistent identifier (PID) by its ARK (Archival Resource Key) identifier.

            Parameters:
                dark_id (str): The ARK identifier of the PID.

            Returns:
                str: The PID associated with the given ARK identifier.
        """
        dark_object = self.dpid_db.caller.get_by_noid(dark_id)

        payload_hash = dark_object[-2]
        
        # b'\x00' * 32 = 0
        if payload_hash != b'\x00' * 32:
            payload_py_obj = self.get_payload(payload_hash)
        else:
            payload_py_obj = None
            # Payload.populate(dark_object)


        return DarkPid.populate(dark_object,self.epid_db,self.url_service,payload_py_obj)
    
    ##
    ## PayloadSchema
    ##
    
    def get_payload_schema_by_hash(self,ps_id:bytes):
        #entra bytes32 a conversao e feita pelo web3
        # assert dark_id.startswith('0x'), "id is not hash"
        dark_object = self.dpid_db.caller.get_payload_schema(ps_id)
        return PayloadSchema.populate(dark_object)
    
    def get_payload_schema_by_name(self,schema_name:str):
        dark_object = self.dpid_db.caller.get_payload_schema(schema_name)
        return PayloadSchema.populate(dark_object)
    
    ##
    ## Payload
    ##

    def get_payload(self,payload_hash_id):
        # assert dark_id.startswith('0x'), "id is not hash"
        dark_object = self.dpid_db.caller.get_payload(Web3.toHex(payload_hash_id))
        payload_schema_hash_id = dark_object[0]
        payload_schema = self.get_payload_schema_by_hash(payload_schema_hash_id)
        return Payload.populate(dark_object,payload_schema)
    
    def validade_payload(self,payload: dict,payload_schema:PayloadSchema):
        errors = []
        for p in payload.keys():
            if p.lower() not in payload_schema.attribute_list:
                errors.append(p)
        
        if len(errors) > 0:
            raise Exception(" Attributes {} not in PayloadSchema {}".format(errors,payload_schema.schema_name))



