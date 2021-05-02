class Blockchin():
    def __init__(self, pow_zeros, leaf_sz):
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.blockchain = []
        
    def add_genesis_block(self,transaction):
        # create a block for this transaction and add it to blockchain list
        block = Block()