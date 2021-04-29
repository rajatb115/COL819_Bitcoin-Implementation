import time
import util

class Transaction():
    def __init__(self,send_money,recieve_money,public_key,private_key,txn_type):
        self.send_money = send_money
        self.recieve_money = recieve_money
        self.public_key = public_key
        self.private_key = private_key
        self.txn_type = txn_type
        self.txn_time = time.time()
        
        # sign the transaction
        self.txn_sign = self.sign_transaction()
        
        
    def txn_message(self):
        message = ""
        # Message should contain the timestamp and the detail of the transaction
        message = message + "Start Time :"str(int(self.txn_time))+" Number of send transactions :"+str(len(self.send_money))+ " Number of recieved transactions :"+str(len(self.recieve_money))
        
        for i in self.send_money:
            message=message+
            
        return message
    
    
    def sign_transaction(self):
        pri_key = util.RSA_to_key(self.private_key)
        return sign_message(txn_message(),pri_key)