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
        self.current_block_hash = ''
        self.root_merkle_tree = self.get_root()
        
    def get_root():
        # root of the merkle tree will be at the end of the 2D list
        return self.merkle_tree[-1][0]
    
    def merkle_tree(self):
        # creating merkle tree of all the records in a transaction.
        lis = []
        for txn in self.transaction:
            lis.append(txn.txn_id)
        
        # return the list (merkle tree)
        return util.create_merkle_tree(lis,self.leaf_sz)
    
    def proof_of_work(self):
        
        if util.get_debug():
            print("Starting proof of work : ")
        
        # current block hash is equal to the hash of (previous block + root of merkle tree + nounce)
        # if first pow_zeros digit of hash is equal to zero then out nounce is true.
        temp_nounce = 0
        message = str(self.root_merkle_tree)+ " " + str(self.prev_block_hash)
        
        # Find the hash of the message + temp_nounce
        message_hash = util.create_hash(message + str(temp_nounce))
        
        # check if the number of pow_zeros digit of message_hash is equal to zero
        while(!self.check_pow_zeros(message_hash)):

            if util.get_debug():
                print("Testing nounce : ",str(temp_nounce)," ; Temp hash of message : ",str(message_hash))
            
            