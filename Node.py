import time
import util
import Miner
import blockchain
import Transaction
from threading import Thread, Event

def get_keys():
    return util.public_private_key()

def get_hash(data):
    val = data.hex()
    return util.create_hash(val)

class Inputs():
    def __init__(self,prev_txid="None",txr_index="None"):
        self.prev_txid = prev_txid
        self.txr_index = txr_index
    
    def __str__(self):
        message = "Inputs : Previous output reference = " + str(self.prev_txid)
        message = message + " ; Prevoius index = " + str(self.txr_index)
        return message
    
class Outputs():
    def __init__(self, to_public_address, amount):
        address = to_public_address.hex()
        self.to_public_address_hash = util.create_hash(address)
        self.amount = amount
    
    def __str__(self):
        message = "Outputs : Hash of receiver = " + str(self.to_public_address_hash)
        message = message + " ; Amount = " + str(self.amount) + " btc"
        return message

class Node():
    
    def __init__(self,idx,node_cnt,pow_zeros,leaf_sz,message_common_list,message_limit):
        
        # common details about a node
        self.idx = idx
        self.node_cnt = node_cnt
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.message_common_list = message_common_list
        self.message_limit = message_limit
        
        # block details
        self.block_create_reward = util.get_block_create_reward()
        self.block_create_time = util.get_block_create_time()
        
        # here public and private key are in binary format
        self.private_key,self.public_key = get_keys()
        
        # hash of public key
        self.hash_public_key = get_hash(self.public_key)
        
        self.bitcoin = 0
        self.unspent_bitcoin = {}
        self.transaction_charges = util.get_transaction_charges()
        
        self.start_time = time.time()
        
        self.dict_public_key_nodeid = {}
        self.nodeid_public_key = []
        self.prev_trans_key = None
        self.prev_trans_verified = False
        self.prev_trans_time = 0
        
        if util.get_debug():
            self.debug()
        
    def debug(self):
        print("")
        print("Printing the details of node")
        print("Node id : ",self.idx)
        print("Node count :",self.node_cnt)
        print("proof of work :",self.pow_zeros)
        print("leaf size of merkle tree :",self.leaf_sz)
        print("common list details :")
        for i in range(len(self.message_common_list)):
            print(self.message_common_list)
        print("Block message limit :",self.message_limit)
        print("Block creation reward :",self.block_create_reward)
        print("Block creation time :",self.block_create_time)
        print("Node Public key :",self.public_key)
        print("Node Private key :",self.private_key)
        print("Node hash of public key :",self.hash_public_key)
        print("Current Bitcoins :",self.bitcoin)
        print("Unspent bitcoins :",self.unspent_bitcoin)
        print("transaction charges :",self.transaction_charges)
        print("")
        
    def find_cash(self):
        sm = 0
        for key in self.unspent_bitcoin.keys():
            sm = sm + self.unspent_bitcon[key][1]
            
        if util.get_debug():
            print("# Coin at Noide :",self.idx, "is",sm)
        return sm
    
        
    def start_transactions(self,q_list,miner):
        
        while True:
            # check if there is any transaction in the queue pending or not
            try:
                message = q_list[self.idx].get(block=True, timeout=1)
                
                if util.get_debug():
                    print("# Found some message in the queue of Node =",self.idx,": Message=",message)
                
                # The recieved message could be a transaction or new block
                if message[0]=="TXN":
                    if util.get_debug():
                        print("# This is transaction message at Node =",self.idx)
                    
                    message_txn = message[1]
                    
                    # verify the transcation
                    if message_txn.check_sign_transaction():
                        if util.get_debug():
                            print("# Trasaction is verified at Node =",self.idx)
                        
                        ##################################
                        # check for duplicate transaction#
                        ##################################
                        
                        miner.current_transactions.append(message_txn)
                    
                    else:
                        if util.get_debug():
                            print("# Trasaction is not verified at Node =",self.idx)
                            
                if message[0] == "BLOCK":
                    
                    if util.get_debug():
                        print("# This is new block message at Node =",self.idx)
                     
                    ######################################
                    # to do add a block in the blockchain#
                    ######################################
            
            except:
                
                reciever = None
                sender = self.idx
                amount = 0
                        
                # check for the smart contract and if the node id is in the smart contract then
                # perform the smart contract
                
                # Getting the nodes which are responsible for smart contract
                smart_contract_nodes =  util.get_smart_contract_nodes()
                
                # Check if current node is participating in the smart contract
                if self.idx in smart_contract_nodes.keys():
            
                    if util.get_smart_contract() and self.find_cash() >= util.get_smart_contract_balance():
                        
                        if util.get_debug():
                            print("Performing smart contract for Node",self.idx)
                            
                        self.message_common_list.append(self.idx)
                        reciever = smart_contract_nodes[self.idx]
                        sender = self.idx
                        amount = util.get_smart_contract_deduction()
                        
                        if util.print_logs():
                            print("")
                            print("Node",sender, "is sending",amount,"btc to Node",reciever,"as a part of smart contract.")
                            print("")
                        
                    else:
                        reciever = util.find_random_reciever(self.node_cnt,self.idx)
                        sender = self.idx
                        amount = util.get_random_amount()
                        
                        if util.print_logs():
                            print("Node",sender, "is sending",amount,"btc to Node",reciever,".")
                        
                else:
                    reciever = util.find_random_reciever(self.node_cnt,self.idx)
                    sender = self.idx
                    amount = util.get_random_amount()
                    
                    if util.print_logs():
                        print("Node",sender, "is sending",amount,"btc to Node",reciever,".")
                
                ##########################
                #### need to complete ####
                ##########################
                
                
                # Calculating time spend till now by the node and halt the process after timeout
                if util.get_debug():
                    print("# Start time=",self.start_time,": Total time=",util.get_total_time(),": Time spent=",time.time()-self.start_time)
                
                if(time.time()-self.start_time>util.get_total_time()):
                    if util.print_logs():
                        print("Node",self.idx,"is halting due to timeout")
                        print("Printing the logs of the Node",self.idx)
                        self.debug()
                    break
                
    def update_bitcoin_details(self , block):
        
        if util.get_debug():
            print("")
            print("# Block is confirmed and updating the details.")
            print("# Node index :",self.idx)
            print("# Length of the block transaction :",len(block.transaction))
            print("")
            
        for i in range(len(block.transaction)):
            txn = block.transaction[i]
            txnid = txn.txn_id
            
            '''
            check all the output transactions of the block and add all the amount 
            '''
            for itr , out in enumerate(txn.txn_output):
                reciever = out.to_public_address_hash
                
                # check if the current node is recieved any bitcoin
                if reciever == self.hash_public_key:
                    
                    # creating a unique key to store this amount to unspent coin
                    temp_key  = str(itr) + str(":") + str(txnid)
                    
                    if util.get_debug():
                        print(self.unspent_bitcoin.keys())
                        print(temp_key)
                        
                    if temp_key not in self.unspent_bitcoin.keys():
                    
                        # if the transaction type is COIN-BASE then this means
                        # this is node creation amount + genesis block creation coin.
                        if txn.txn_type == "COIN-BASE":
                            
                            # If it is node 0 then it will have initial amount + block creation reward
                            if self.idx==0:
                                if (util.print_logs()):
                                    print("Node "+str(self.idx)+" recieved " +str(out.amount-self.block_create_reward)+ " btc as initial node amount.")
                                    print("Node "+str(self.idx)+" recieved "+str(self.block_create_reward) + " btc as Genesis block creation reward.")
                        
                            # If the node is not node 0 then it won't recieve the block creation reward
                            else:
                                if (util.print_logs()):
                                    print("Node "+str(self.idx)+" recieved " +str(out.amount)+ " btc as initial node amount.")
                                    
                            self.bitcoin = self.bitcoin + out.amount
                            self.unspent_bitcoin[temp_key] = [None, out.amount, txnid, itr]
                        
                        # if the transsaction type is not COIN-BASE            
                        else:
                            #If money is recieved from some other node
                            sender = self.dict_public_key_nodeid[txn.public_key]
                            if (self.idx != sender):
                                if (util.print_logs()):
                                    print("Node "+str(self.idx)+" recieved "+str(out.amount)+" from Node "+str(sender))
                                    
                                self.bitcoin = self.bitcoin + out.amount
                                self.unspent_bitcoin[temp_key] = [txn.public_key, out.amount, txnid, itr]
                                
                    else:
                        if util.print_logs():
                            print("This transaction has already been accounted.")
            
            # Now subtract the spend money from the bitcoin
            sender = self.dict_public_key_nodeid[txn.public_key]
            reciever = self.public_key
            # for coinbase transaction the input is none so avoid that 
            if (sender != reciever):
                if(txn.txn_type != "COIN-BASE"):
                    '''
                    check all the input transactions of the block and subtract the amount
                    '''
                    for itr, inp in enumerate(txn.txn_input):
                        temp_key = str(itr)+str(":")+str(inp.prev_txid)
                        
                        # subtract the bitcoin for the above key 
                        self.bitcoin = self.bitcoin - self.unspent_bitcoin[temp_key][1]
                        del self.unspent_bitcoin[temp_key]
                        
                        # if detail of the output is present in the input list then key will match
                        if self.prev_trans_key != None and temp_key == self.prev_trans_key:
                            # If key match then this means it is validated
                            self.prev_trans_verified = True
                            self.last_trans_key = None
                            if util.print_logs():
                                print("Time taken by Node",self.idx,"for transaction verification is",time.time()-self.prev_trans_time)
                    
                else:
                    if util.get_debug():
                        print("COIN-BASE: Transaction no input found.")
                
            
    def run_node(self,q_list):
        
        # All nodes will share their public key to eachother
        self.nodeid_public_key = []
        
        for i in range(self.node_cnt):
            if i!= self.idx:
                self.nodeid_public_key.append(None)
            else:
                self.nodeid_public_key.append(self.public_key)
                self.dict_public_key_nodeid[self.public_key] = self.idx

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
                    self.nodeid_public_key[msg_lis[2]] = msg_lis[1]
                    self.dict_public_key_nodeid[msg_lis[1]] = msg_lis[2]
                    temp += 1
            except:
                if util.get_debug():
                    print("Still waiting....")
                pass
            
        if util.get_debug():
            print("Reading of public key for node ",self.idx," is completed")
            print(self.nodeid_public_key,"\n")
        
        
        '''
        Creating an instance of miner for this node. All the nodes will act as miners.
        Since this node know each of the available node thus it can start mining. 
        '''
        
        miner = Miner.Miner(self.idx, self.node_cnt, self.pow_zeros, self.leaf_sz, self.private_key, self.nodeid_public_key, self.block_create_reward, self.block_create_time, self.transaction_charges)
        
        
        '''
        After public key distribution a node will distribute money to all the node and add a
        genesis block for these transactions. Let this block is added by the node whose nodeId is 0 (self.idx=0).
        '''
        
        # node 0 is creating the genesis block
        if(self.idx == 0):
            
            if util.get_debug():
                print("idx of the current node :",str(self.idx))
            
            # create a initial block chain
            block_chain = blockchain.Blockchain(self.pow_zeros, self.leaf_sz)
            miner.blockchain = block_chain
            
            # it will refer to the previous output
            tx_inputs = []
            # current output
            tx_outputs = []
            
            tx_inputs.append(Inputs())
            
            for i in range(int(self.node_cnt)):
                initial_amt = util.get_initial_amount()
                
                # node 0 will add the genesis block so will get block creation reward
                if i==0:
                    initial_amt = initial_amt + self.block_create_reward
                
                out = Outputs(self.nodeid_public_key[i],initial_amt)
                tx_outputs.append(out)
                
                if util.get_debug():
                    print("Adding money in btc :",initial_amt," to node :",i)
            
            # create a transaction for these statments
            transaction = Transaction.Transaction(tx_inputs, tx_outputs, self.public_key, self.private_key, "COIN-BASE" )
            
            # Start genesis block creation time
            if util.print_logs():    
                gblock_time = time.time()
            
            # creating and adding the genesis block
            miner.blockchain.add_genesis_block([transaction])
            
            # Printing the log 
            if util.print_logs():
                print("Time taken to create Genesis block : ",str(time.time()-gblock_time))
                
            '''
            # Update the unspend bitcoin for the current node do if 
            # the block is confirmed and since it is genesis block we assume that it is confirmed
            '''
            
            genesis_blockchain = miner.blockchain
            self.update_bitcoin_details(genesis_blockchain.blockchain[0])
            
            # Pushing the genesis block into stack so that all the nodes can read it
            for i in range(self.node_cnt):
                if i != 0:
                    if util.print_logs():
                        print("Node 0 is pushing the genesis block to the stack of node : ",i)
                    
                    q_list[i].put(["GENESIS-BLOCK",miner.blockchain,self.idx,i])
            
            if util.get_debug():
                self.debug()
            
        
        # Now rest of the node take this genesis block as the initial block and store it in their
        # respective blockchain list
        else:
            message = None
            temp = True
            while temp:
                try:
                    message = q_list[self.idx].get(block=True, timeout=5)
                    if util.get_debug():
                        if message != None:
                            print("# Node",self.idx,"recieved some message.")
                            print("# Message :",message)
                            
                except:
                    if util.print_logs():
                        print("Node",self.idx,"Waiting for the Genesis block.")
                        
                # check if the message is about genesis block or not
                if message[0]=="GENESIS-BLOCK":
                        
                    # if this node got the message then stop the while loop
                    if message != None:
                        temp = False
                    
                    miner.blockchain = message[1]
                    
                    if util.print_logs():
                        print("Node",self.idx,"recieved the Genesis Block from Node 0.")
                    
                    # Now verify the block which is recieved
                    if (miner.is_valid_block("GENESIS-BLOCK",None)):
                        
                        if util.print_logs():
                            print("Node",self.idx,"Genesis block transactions are verified.")
                            
                        genesis_blockchain = miner.blockchain
                        self.update_bitcoin_details(genesis_blockchain.blockchain[0])
            if util.get_debug():
                self.debug()
                    
        '''
        Now the nodes will perform transactions between each other and a block for those transactions will  be stored in the blockchain.
        '''
        
        # creating thread for transaction and mining
        txn_thread = Thread(target=self.start_transactions(q_list,miner), name='Txn:'+str(self.idx))
        txn_thread.start()
        txn_thread.join()
        
        #self.start_transactions(q_list,miner)
        
        
        