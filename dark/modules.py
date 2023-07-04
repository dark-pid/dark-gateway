from .gateway import DarkGateway
from .util import invoke_contract_sync

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
        self.sete_db = dark_gateway.deployed_contracts_dict['SearchTermDB.sol']
        # authorities db to configuration
        self.auth_db = dark_gateway.deployed_contracts_dict['AuthoritiesDB.sol']
        #dARK services
        self.dpid_service = dark_gateway.deployed_contracts_dict['PIDService.sol']
        self.epid_service = dark_gateway.deployed_contracts_dict['ExternalPIDService.sol']
        self.sets_service = dark_gateway.deployed_contracts_dict['SearchTermService.sol']
        self.auth_service = dark_gateway.deployed_contracts_dict['AuthoritiesService.sol']
    
    
    ###
    ### Request PID
    ###

    def request_pid_hash(self):
        """
            Request a PID and return the hash (address) of the PID
        """
        signed_tx = self.gw.signTransaction(self.dpid_service , 'assingID', self.gw.authority_addr)
        r_tx, receipt = invoke_contract_sync(self.gw,signed_tx)
        dark_id = r_tx['logs'][0]['topics'][1]
        return dark_id
    
    def request_pid(self):
        """
            Request a PID and return the ark of the PID
        """
        return self.convert_pid_hash_to_ark(self.request_pid_hash())
    
    def convert_pid_hash_to_ark(self,dark_pid_hash):
        """
            Convert the dark_pid_hash to a ARK identifier
        """
        return self.dpid_db.caller.get(dark_pid_hash)[1]
    


