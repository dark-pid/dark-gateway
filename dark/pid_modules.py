from web3 import Web3
# from web3._utils.datatypes import Contract

class DarkPid:

    def __init__(self,pid_hash,ark_id,externa_pid_list,payload,owner) -> None:
        self.pid_hash = pid_hash
        self.ark = ark_id
        self.externa_pid_list = externa_pid_list
        self.payload = payload
        self.responsible = owner
    
    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)
    
    def __is_bc_valid(bc_output):
        """
        Validates the structure and types of the provided output.

        Parameters:
            output (tuple): The output to be validated.

        Returns:
            bool: True if the output is valid, False otherwise.
        """

        if len(bc_output) != 10:
            return False

        if not isinstance(bc_output[0], bytes) or not isinstance(bc_output[1], str):
            return False

        if not isinstance(bc_output[2], list) or not isinstance(bc_output[3], list):
            return False

        if not isinstance(bc_output[4], int) or not isinstance(bc_output[5], list):
            return False

        if not isinstance(bc_output[6], int) or not isinstance(bc_output[7], tuple):
            return False

        if not isinstance(bc_output[8], str) or not isinstance(bc_output[9], str):
            return False

        return True


    def populateDark(dark_object,epid_db_contract):
        assert DarkPid.__is_bc_valid(dark_object) == True, "Invalid Blockchain Output"
        # TODO: VALIDADE epid_db_contract
        # assert type(epid_db_contract) == Contract, "epid_db_contract must be web3._utils.datatypes.Contract type"

        # populate external pids
        external_pids = []
        for ext_pid in dark_object[3]:
            ext_pid = Web3.toHex(ext_pid)
            # epid = epid_db.functions.get(ext_pid).call()
            get_func = epid_db_contract.get_function_by_signature('get(bytes32)')
            epid = get_func(ext_pid).call()

            pid_object = {'id': ext_pid, 
                            'schema:' : epid[3] , 'value' : epid[2], 
                            'owner:' : epid[-1]
                        }
            external_pids.append(pid_object)
        
        # deprecated
        # external_links = []
        # for ext_link in dark_object[5]:
        #     external_links.append(ext_link)

        pid_hash_id = Web3.toHex(dark_object[0])
        pid_ark_id = dark_object[1]
        payload = dark_object[-2]
        owner = dark_object[-1]
        

        return DarkPid(pid_hash_id,pid_ark_id,external_pids,payload,owner)

        


class ExeternalPid:
    def __init__(self,id_hash,schema,value,creator) -> None:
        self.id = id_hash
        self.schema = schema
        self.pid_str_value = value
        self.creator_addr = creator

    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)