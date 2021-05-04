import util
import Block

class Blockchain():
    def __init__(self, pow_zeros, leaf_sz):
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.blockchain = []
        
        if util.get_debug():
            self.debug()
        
    def debug(self):
        print("")
        print("Inside Blockchain")
        print("Blockchain : proof of work -",self.pow_zeros)
        print("Blockchain : leaf size -",self.leaf_sz)
        print("")
        
    def add_genesis_block(self,transaction):
        # create a block for this transaction and add it to blockchain list
        if util.get_debug():
            print("Started adding the genesis block")
        block = Block.Block(self.pow_zeros, self.leaf_sz, transaction, "GENESIS-BLOCK","0",0)