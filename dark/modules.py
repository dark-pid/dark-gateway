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
        self.payload_schema_db = dark_gateway.deployed_contracts_dict['PayloadSchemaDB.sol']
        # authorities db to configuration
        self.auth_db = dark_gateway.deployed_contracts_dict['AuthoritiesDB.sol']
        #dARK services
        self.dpid_service = dark_gateway.deployed_contracts_dict['PIDService.sol']
        self.epid_service = dark_gateway.deployed_contracts_dict['ExternalPIDService.sol']
        self.url_service = dark_gateway.deployed_contracts_dict['UrlService.sol']
        self.auth_service = dark_gateway.deployed_contracts_dict['AuthoritiesService.sol']
        self.payload_schema_service = dark_gateway.deployed_contracts_dict['PayloadSchemaService.sol']
        #payload schema name
        # self.payload_schema_name = dark_gateway.payload_schema_name
    
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
    
    def __create_payload_schema(self,shcema_name:str,version:str,confiured:bool):
        """
            Create a payload schema and return the hash (address) of the payload
        """
        return self.gw.signTransaction(self.payload_schema_service , 
                                       'get_or_create_payload_schema',
                                       shcema_name, version, confiured)
   
    def __set_payload(self,pid_hash:HexBytes,payload_schema:HexBytes,payload_addr):
        assert type(pid_hash) == HexBytes, "pid_hash must be a HexBytes object"

        # function set_payload(bytes32 pid_hash,
        #             bytes32 payload_schema,
        #             bytes32 payload_hash)
        # print(type(pid_hash),type(payload_schema),type(payload_addr))
        # print(payload_schema)
        signed_tx = self.gw.signTransaction(self.dpid_service , 'set_payload', 
                                            pid_hash,
                                            # HexBytes(payload_schema),
                                            payload_schema,
                                            payload_addr
                                            )
        
        return signed_tx      
    

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
        # print(receipt)
        dark_id = receipt['logs'][0]['topics'][1]
        return dark_id
    
    def bulk_request_pid_hash(self,gas=3000000):
        """
            Request a PID and return the hash (address) of the PID
        """
        # orginal
        # signed_tx = self.gw.signTransaction(self.dpid_service , 'bulk_assingID', self.gw.authority_addr)

        #temp
        tx_params = self.gw.get_tx_params(gas)
        tx = self.dpid_service.get_function_by_name('bulk_assingID')(self.gw.authority_addr).build_transaction(tx_params)
        signed_tx = self.gw.signTx(tx)

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
    
    def sync_create_payload_schema(self,shcema_name:str,version:str,confiured:bool):
        """
            Create a payload schema and return the hash (address) of the payload
        """
        signed_tx = self.__create_payload_schema(shcema_name,version,confiured)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        # return receipt['logs']
        return receipt['logs'][0]['topics'][1].hex()
    
    def sync_set_payload(self,hash_pid:HexBytes,payload_schema:HexBytes,payload_addr:str):
        # def __set_payload(self,pid_hash:HexBytes,payload_schema:HexBytes,payload_addr):
        signed_tx = self.__set_payload(hash_pid,payload_schema,payload_addr)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        return r_tx
    

        
    
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
    
    def async_set_payload(self,hash_pid:HexBytes,payload_schema:HexBytes,payload_addr:str):
        # def __set_payload(self,pid_hash:HexBytes,payload_schema:HexBytes,payload_addr):
        signed_tx = self.__set_payload(hash_pid,payload_schema,payload_addr)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx


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
        # Payload
        raw_payload = dark_object[4]
        if (raw_payload[0]!= b'\x00' * 32) and (raw_payload[1]!= b'\x00' * 32):
            payload_schema = self.get_payload_schema_by_hash(raw_payload[0])
            payload_py_obj = Payload(payload_schema=payload_schema,payload_addr=raw_payload[1])
        else:
            payload_py_obj = None

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

        # Payload
        raw_payload = dark_object[4]
        if (raw_payload[0]!= b'\x00' * 32) and (raw_payload[1]!= b'\x00' * 32):
            payload_schema = self.get_payload_schema_by_hash(raw_payload[0])
            payload_py_obj = Payload(payload_schema=payload_schema,payload_addr=raw_payload[1])
        else:
            payload_py_obj = None

        return DarkPid.populate(dark_object,self.epid_db,self.url_service,payload_py_obj)
    
    ##
    ## PayloadSchema
    ##
    
    def get_schema_hash_id(self,schema_name:str,schema_version:str):
        """
            Retrieves the hash of a payload schema by its name and version.

            Parameters:
                schema_name (str): The name of the payload schema.
                schema_version (str): The version of the payload schema.

            Returns:
                str: The hash of the payload schema.
        """
        return '0x'+ self.payload_schema_db.caller.gen_schema_id(schema_name,schema_version).hex()
    
    def get_payload_schema_by_hash(self,ps_id:bytes):
        """
            Retrieves the payload schema by its hash.

            Parameters:
                ps_id (str): The hash of the payload schema.

            Returns:
                PayloadSchema: The payload schema object.
        """
        #entra bytes32 a conversao e feita pelo web3
        # assert dark_id.startswith('0x'), "id is not hash"
        dark_object = self.payload_schema_service.caller.get(ps_id)
        ps = PayloadSchema.populate(dark_object)
        ps.set_id(ps_id)

        return ps
    
    def get_payload_schema_by_name(self,schema_name:str,schema_version:str):
        """
            Retrieves the payload schema by its name and version.

            Parameters:
                schema_name (str): The name of the payload schema.
                schema_version (str): The version of the payload schema.

            Returns:
                PayloadSchema: The payload schema object.
        """
        
        return self.get_payload_schema_by_hash(self.get_schema_hash_id(schema_name,schema_version))
    
    ##
    ## Payload
    ##
    
    # def get_payload(self,payload_hash_id):
    #     # assert dark_id.startswith('0x'), "id is not hash"
    #     dark_object = self.dpid_db.caller.get_payload(Web3.to_hex(payload_hash_id))
    #     payload_schema_hash_id = dark_object[0]
    #     payload_schema = self.get_payload_schema_by_hash(payload_schema_hash_id)
    #     return Payload.populate(dark_object,payload_schema)
    
    # def validade_payload(self,payload: dict,payload_schema:PayloadSchema):
    #     errors = []
    #     for p in payload.keys():
    #         if p.lower() not in payload_schema.attribute_list:
    #             errors.append(p)
        
    #     if len(errors) > 0:
    #         raise Exception(" Attributes {} not in PayloadSchema {}".format(errors,payload_schema.schema_name))



