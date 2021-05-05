import util
import Block

class Blockchain():
    def __init__(self, pow_zeros, leaf_sz):
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.blockchain = []
        self.utox = set()
        
        if util.get_debug():
            self.debug()
        
    def debug(self):
        print("")
        print("Inside Blockchain")
        print("Blockchain : proof of work -",self.pow_zeros)
        print("Blockchain : leaf size -",self.leaf_sz)
        print("Unspent transactions -",str(self.utox))
        print("")
    
    def add_UTXO(self,transaction):
        for txn in transaction:
            for i in range (len(txn.txn_output)):
                message = 
    
    def add_genesis_block(self,transaction):
        # create a block for this transaction and add it to blockchain list
        if util.get_debug():
            print("# Starting adding the genesis block by node 0 :")
            
        block = Block.Block(self.pow_zeros, self.leaf_sz, transaction, "GENESIS-BLOCK","0",0)
        
        if util.get_debug():
            print("# Completed the creation of block")
        
        # Listing the unspend transactions
        self.add_UTXO(transaction)
        
    
    def add_block(self,transaction):
        
        
        