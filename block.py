




class block():
    def __init__(self, ):
        self.pow_zero = pow_zero
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.block_type = block_type
        
        self.block_type = block_type
        self.previous_block_hash = previous_block_hash
        self.narry = narry
        self.index = index
        self.pow_number_of_zeros = proof_of_work_zeros
        self.transactions = transactions
        self.transactions_count = len(self.transactions)
        self.merkle_tree = create_merkle_tree([item.txid for item in self.transactions],self.narry,hash_type) #### given the list of transactions, create their hashes and get the merkle tree
        self.merkle_tree_root = self.merkle_tree[-1][0]