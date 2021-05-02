import time
import util

def get_debug_():
    return True

def get_keys():
    return util.public_private_key()

def get_hash(data):
    val = data.hex()
    return util.create_hash(val)

class Node():
    
    def __init__(self,idx,node_cnt,pow_zeros,leaf_sz,common_list,message_limit):
        
        # common details about a node
        self.idx = idx
        self.node_cnt = node_cnt
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.common_list = common_list
        self.message_limit = message_limit
        
        # block details
        self.block_create_reward = 5
        self.block_create_time = 20
        
        # here public and private key are in binary format
        self.private_key,self.public_key = get_keys()
        
        # hash of public key
        self.hash_public_key = get_hash(self.public_key)
        
        self.bitcoins = 0
        self.unspent_bitcoin = {}
        self.transaction_charges = 1
        
        self.start_time = time.time()
        
        if get_debug_():
            self.debug()
        
    def debug(self):
        print("Printing the details of node")
        print("Node id : ",self.idx)
        print("Node count :",self.node_cnt)
        print("proof of work :",self.pow_zeros)
        print("leaf size of merkle tree :",self.leaf_sz)
        print("common list details :")
        for i in range(len(self.common_list)):
            print(self.common_list)
        print("Block message limit :",self.message_limit)
        print("Block creation reward :",self.block_create_reward)
        print("Block creation time :",self.block_create_time)
        print("Node Public key :",self.public_key)
        print("Node Private key :",self.private_key)
        print("Node hash of public key :",self.hash_public_key)
        print("Current Bitcoins :",self.bitcoins)
        print("Unspent bitcoins :")
        for i in self.unspent_bitcoin:
            print(i)
        print("transaction charges :",self.transaction_charges)
        print("")
        
    def run_node(self,q_list):
        
        # All nodes will share their public key to eachother
        self.node_public_key = []
        
        for i in range(self.node_cnt):
            if i!= self.idx:
                self.node_public_key.append(None)
            else:
                self.node_public_key.append(self.public_key)

        # Broadcast my public key to all the nodes so a node will need (n-1) messages to put in
        # the shared memory of each node
        for i in range(self.node_cnt):
            if i != self.idx:
                q_list[i].put(["PK",self.public_key,self.idx])
        
        # read the public key of other nodes in the network
        temp = 1
        while(temp < self.node_cnt):
            try:
                msg_lis = q_list[self.idx].get(block=True,timeout=20)
                #print(msg_lis)
                if msg_lis[0] == "PK":
                    self.node_public_key[msg_lis[2]] = msg_lis[1]
                    temp += 1
            except:
                if get_debug_():
                    print("Still waiting....")
                pass
            
        if get_debug_():
            print("Reading of public key for node ",self.idx," is completed")
            print(self.node_public_key,"\n")
        
        
        '''
        Creating an instance of miner for this node. All the nodes will act as miners.
        Since this node know each of the available node thus it can start mining. 
        '''
        
        miner = Miner(self.idx, self.node_cnt, self.pow_zeros, self.leaf_sz, self.private_key, self.node_public_key, self.block_create_reward, self.block_create_time, self.transaction_charges)
        
        
        '''
        After public key distribution a node will distribute money to all the node and add a
        genesis block for these transactions. Let this block is added by the node whose nodeId is 0 (self.idx=0).
        '''
        
        # node 0 is creating the genesis block
        if self.idx == 0:
            recieve_money = []
            send_money = []
            
            for i in range(self.node_cnt):
                initial_amt = 5000
                
                # node 0 will add the genesis block so will get block creation reward
                if i==0:
                    initial_amt = initial_amt + self.block_create_reward
                
                send_money.append([self.node_public_key[i].hex(),initial_amt])
                
            # create a transaction for these statments
            transaction = Transaction(send_money, recieve_money, self.public_key, self.private_key, "COINBASE" )
            
            # create a initial block chain blockchain
            miner.blockchain = Blockchain(self.pow_zeros, self.leaf_sz)
            
            # Start genesis block creation time
            if util.print_logs():    
                gblock_time = time.time()
            
            # add the genesis block
            miner.blockchain.add_genesis_block([transaction])
            
            if util.print_logs():
                print("Time taken to create Genesis block : ",str(time.time()-fblock_time))
            
            
            
                
                
        
        '''
        Now the nodes will do transaction with each other the will be stored in the blockchain.
        '''
