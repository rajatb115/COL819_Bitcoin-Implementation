import util

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
        
        self.blockchain = None
        
        if util.get_debug():
            self.debug()
    
    def debug(self):
        print("")
        print("Printing the details of Miner")
        print("Node id : ",self.idx)
        print("Node count :",self.node_cnt)
        print("proof of work :",self.pow_zeros)
        print("leaf size of merkle tree :",self.leaf_sz)
        print("Private key of node :",self.private_key)
        print("list of public key of other nodes :",self.node_public_key)
        print("Block creation reward :",self.block_create_reward)
        print("Block creation time :",self.block_create_time)
        print("Transaction charge :",self.transaction_charges)
        print("Blockchain :",self.blockchain)
        print("\n")
    
    
    # Function to check whether the genesis block is valid or not
    def is_valid_genesis_block(self):
        
        if util.get_debug():
            print("# Miner",self.idx": Verifying the genesis block.")
            
        
        
