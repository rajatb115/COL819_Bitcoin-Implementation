import util
import sys

class Miner():
    def __init__(self, idx, node_cnt, pow_zeros, leaf_sz, private_key, node_public_key, block_create_reward, block_create_time, transaction_charges):
        
        self.idx = idx
        self.node_cnt = node_cnt
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.private_key = private_key
        self.node_public_key = node_public_key
        self.block_create_reward = block_create_reward
        self.block_create_time = block_create_time
        self.transaction_charges = transaction_charges
        
        self.current_transactions = []
        
        self.blockchain = None
        
        if util.get_debug():
            self.debug()
    
    def debug(self):
        print("")
        print("# Printing the details of Miner")
        print("# Node id : ",self.idx)
        print("# Node count :",self.node_cnt)
        print("# proof of work :",self.pow_zeros)
        print("# leaf size of merkle tree :",self.leaf_sz)
        print("# Private key of node :",self.private_key)
        print("# list of public key of other nodes :",self.node_public_key)
        print("# Block creation reward :",self.block_create_reward)
        print("# Block creation time :",self.block_create_time)
        print("# Transaction charge :",self.transaction_charges)
        print("# Blockchain :",self.blockchain)
        print("# Current transactions :",self.current_transactions)
        print("\n")
    
    
    def add_new_block(self, block):
        
        # check if block is geniune or not check its transactions
        for txn in block.transaction:
            for inps in txn.txn_input:
                if txn.txn_type != "COIN-BASE"  and  txn.txn_type != "REWARD":
                    if self.blockchain.UTXO(inps.txr_index, inps.prev_txid) not in self.blockchain.utxo:
                        return False
            if (txn.check_sign_transaction() == False):
                return False
                
        
        # check if block is geniune or not check its proof of work 
        if block.is_valid_proof_of_work():
            self.blockchain.height_of_current_block = self.blockchain.height_of_current_block +1
            self.blockchain.blockchain.append(block)
            
            
            #print("lis ll",len(self.current_transactions))
            
            for txn in block.transaction:
                for idx , tx in enumerate(self.current_transactions):
                    if tx.txn_id == txn.txn_id:
                        self.current_transactions.pop(idx)
            
            #print("lis l",len(self.current_transactions))
            return True
        return False
            
    
    def get_amount(self,ins):
        for i in range(self.blockchain.index_of_confirmed_block+1):
            block = self.blockchain.blockchain[i]
            for txn in block.transaction:
                if txn.txn_id == ins.prev_txid:
                    
                    if util.get_debug(): 
                        print("# Found the transaction id")
                        
                    return txn.txn_output[ins.txr_index].amount
                
    def is_verified_block(self):
        if (self.blockchain.height_of_current_block - self.blockchain.index_of_confirmed_block >= 1):
            self.blockchain.index_of_confirmed_block = self.blockchain.height_of_current_block
            return True
        return False
        
        
    # Function to check whether the  block is valid or not
    def is_valid_block(self,block_type,block = None):
        
        # check if the block is genesis block or not
        if block_type == "GENESIS-BLOCK":
            if util.get_debug():
                print("# Miner",self.idx,": Verifying the genesis block.")
            
            # check the proof of work is valid or not
            # verify the transactions is valid or not
            temp_pow_isvalid = self.blockchain.blockchain[0].is_valid_proof_of_work()
            
            if util.get_debug():
                print("# Miner",self.idx,":Proof of work validity :",temp_pow_isvalid)
            
            #temp_txn_is_valid = self.blockchain.isValid_transaction(blockchain[0])
            temp_txn_is_valid = True
            for txn in self.blockchain.blockchain[0].transaction:
                temp_txn_is_valid = temp_txn_is_valid and self.blockchain.isValid_transaction(txn)
                    
            if util.get_debug():
                print("# Miner",self.idx,":Proof of transaction validity :",temp_txn_is_valid)
            
            return (temp_pow_isvalid and temp_txn_is_valid)
            
        else:
            # have to complete to do
            print("This is not a genesis block")
            
    def blockchain_size(self):
        return sys.getsizeof(self.blockchain)