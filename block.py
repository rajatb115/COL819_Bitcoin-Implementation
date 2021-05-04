import util

class block():
    def __init__(self, pow_zeros, leaf_sz, transaction, b_type, prev_block_hash, index):
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.transaction = transaction
        self.b_type = b_type
        self.prev_block_hash = prev_block_hash
        self.merkle_tree = self.merkle_tree()
        self.index = index
        self.nounce = self.proof_of_work()
        
    def merkele_tree(self):
        lis = []
        for txn in self.transaction:
            lis.append(txn.txn_id)
        
        return util.create_merkle_tree(lis,self.leaf_sz)
    
    def proof_of_work(self):
        # current block hash is equal to the hash of (previous block + root of merkle tree + nounce)
        # if first pow_zeros digit of hash is equal to zero then out nounce is true
        
        
    
            
        