from hexbytes.main import HexBytes

from .gateway import DarkGateway
from .util import invoke_contract_sync, invoke_contract_async
from .pid_modules import DarkPid


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
    
    ###################################################################
    ###################################################################
    ###################### SYNC METHODS ###############################
    ###################################################################
    ###################################################################

    ###
    ### Request PID
    ###

    def sync_request_pid_hash(self):
        """
            Request a PID and return the hash (address) of the PID
        """
        signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        dark_id = receipt['logs'][0]['topics'][1]
        return dark_id
    
    def sync_request_pid(self):
        """
            Request a PID and return the ark of the PID
        """
        return self.convert_pid_hash_to_ark(self.sync_request_pid_hash())
    
    def sync_add_external_pid(self,hash_pid: HexBytes,external_pid: str):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'addExternalPid', hash_pid, 0 , external_pid)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        return self.convert_pid_hash_to_ark(hash_pid)
    
    def sync_set_url(self,hash_pid: HexBytes,ext_url: str):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'set_url', hash_pid, ext_url)
        receipt, r_tx = invoke_contract_sync(self.gw,signed_tx)
        return self.convert_pid_hash_to_ark(hash_pid)
    
    def sync_set_payload(self,hash_pid: HexBytes,pay_load: dict):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'set_payload', hash_pid, str(pay_load) )
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
        signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_external_pid(self,hash_pid: HexBytes,external_pid: str):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'addExternalPid', hash_pid, 0 , external_pid)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_url(self,hash_pid: HexBytes,ext_url: str):
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'set_url', hash_pid, ext_url)
        r_tx = invoke_contract_async(self.gw,signed_tx)
        return r_tx
    
    def async_set_payload(self,hash_pid: HexBytes,pay_load: dict):
        
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
        assert type(hash_pid) == HexBytes, "hash_pid must be a HexBytes object"
        signed_tx = self.gw.signTransaction(self.dpid_service , 'set_payload', hash_pid, str(pay_load) )
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
    
    
    
    
    ###
    ### Onchain core queries
    ###

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
        return DarkPid.populateDark(dark_object,self.epid_db,self.url_service)

    def get_pid_by_ark(self,dark_id):
        """
            Retrieves a persistent identifier (PID) by its ARK (Archival Resource Key) identifier.

            Parameters:
                dark_id (str): The ARK identifier of the PID.

            Returns:
                str: The PID associated with the given ARK identifier.
        """
        dark_object = self.dpid_db.caller.get_by_noid(dark_id)
        return DarkPid.populateDark(dark_object,self.epid_db,self.url_service)


