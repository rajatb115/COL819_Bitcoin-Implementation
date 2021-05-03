import util

class block():
    def __init__(self, pow_zero, leaf_sz,  b_type):
        self.pow_zero = pow_zero
        self.leaf_sz = leaf_sz
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.b_type = b_type
        self.prev_block_hash = prev_block_hash
        self.merkle_tree = self.merkle_tree()
        
        
    def merkele_tree(self):
        lis = []
        for transaction in self.transactions:
            
        