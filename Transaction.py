import time
import util

class Transaction():
    def __init__(self, txn_input, txn_output, public_key, private_key, txn_type):
        self.txn_output = txn_output
        self.txn_input = txn_input
        self.public_key = public_key
        self.private_key = private_key
        self.txn_type = txn_type
        self.txn_time = time.time()
        
        # sign the transaction
        self.txn_sign = self.sign_transaction()
        
        # get the hash of the transaction
        self.txn_id = self.getTxn_id()
        
    def getTxn_id(self):
        message = self.txn_message()
        return util.create_hash(message)
    
    def get_total_txn_output(self):
        return len(self.txn_output)
    
    def get_total_txn_input(self):
        return len(self.txn_input)
        
    def txn_message(self):
        message = ""
        # Message should contain the timestamp and the detail of the transaction
        message = message + "Start Time :" + str(int(self.txn_time))+" Number of txn_output:"+str(len(self.txn_output))+ " Number of txn_input transactions :"+str(len(self.txn_input)) + " Sender :" + str(self.public_key)
        
        # All the message
        for i in self.txn_output:
            message = message + str(i)
        for i in self.txn_input:
            message = message + str(i)
        
        if util.get_debug():
            print("txn_message : ",str(message))
        
        return message
    
    def sign_transaction(self):
        pri_key = util.RSA_to_key(self.private_key)
        return util.sign_message(self.txn_message(),pri_key)
    
    def check_sign_transaction(self):
        key = util.RSA_to_key(self.public_key)
        return util.verify_message(self.txn_message(),self.self.txn_sign,key)
