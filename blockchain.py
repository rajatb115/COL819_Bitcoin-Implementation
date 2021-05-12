import util
import Block

class Blockchain():
    def __init__(self, pow_zeros, leaf_sz):
        self.pow_zeros = pow_zeros
        self.leaf_sz = leaf_sz
        self.blockchain = []
        self.utxo = set()
        self.utxo_mapping = dict({})
        self.index_of_confirmed_block = None
        self.height_of_current_block = None
        
        if util.get_debug():
            self.debug()
        
    def debug(self):
        print("")
        print("Inside Blockchain")
        print("Blockchain : proof of work -",self.pow_zeros)
        print("Blockchain : leaf size -",self.leaf_sz)
        print("Unspent transactions -",str(self.utxo))
        print("UTXO mapping :")
        for i in self.utxo_mapping.keys():
            print(i," - ",self.utxo_mapping[i])
        print("Index of the confirmed block -",self.index_of_confirmed_block)
        print("Height of the current block -",self.height_of_current_block)
        print("Blockchain list")
        for i in self.blockchain:
            print(i)
        
        print("")
        
    def UTXO(self, index, txn_hash):
        message = str(index)+ " : " + str(txn_hash)
        return message
    
    def isValid_transaction(self,txn):
        inputs = 0
        outputs = 0
        
        utxo_t = set()
        
        if txn.txn_type == "COIN-BASE":
            return True
        
        for i in range(txn.get_total_txn_input()):
            input_tx = txn.txn_input[i]
            utxo_temp = self.UTXO(input_tx.txr_index,input_tx.prev_txid)
            if not utxo_temp in self.utxo:
                return False
            if utxo_temp in utxo_t:
                return False

            output_txn = self.utxo_mapping[utxo_temp]

            utxo_t.add(utxo_temp)

            inputs = inputs + output_txn.amount
            
        for i in range(txn.get_total_txn_output()):
            output_txn = txn.txn_output[i]
            if output_txn.amount < 0:
                return False
            outputs = outputs + output_txn.amount
            
        return inputs>=outputs


    def add_UTXO(self, transaction):
        try:
            for txn in transaction:
                if self.isValid_transaction(txn):
                    
                    if util.get_debug():
                        print("# This transaction is valid.")
                    
                    for idx in range (len(txn.txn_output)):
                        index = idx
                        txn_hash = txn.txn_id
                        self.utxo.add(self.UTXO(index,txn_hash))
                        self.utxo_mapping[self.UTXO(index,txn_hash)] = txn.txn_output[index]
                else:
                    if util.get_debug():
                        print("# There is a false transaction.")
                    
        except Exception as e:
            print(e)
            return False
        return True
                
    def add_genesis_block(self,transaction):
        # create a block for this transaction and add it to blockchain list
        if util.get_debug():
            print("# Starting adding the genesis block by node 0 :")
            
        block = Block.Block(self.pow_zeros, self.leaf_sz, transaction, "GENESIS-BLOCK","0",0)
        
        if util.get_debug():
            print("# Completed the creation of block")
            
        # Adding the Genesis block to the blockchain
        self.blockchain.append(block)
        
        # Listing the unspend transactions
        temp = self.add_UTXO(transaction)
        
        # check whether it is added succesfully or not
        if (temp == False and util.get_debug()):
            print("# Unable to add the UTXOS for transaction.")
        if (temp == True and util.get_debug()):
            print("# Add the UTXOS for transaction successfully.")
            
        # block number 0 is the genesis block and it is confirmed initially
        self.index_of_confirmed_block = 0
        
        # block 0 is the genesis block and its height is 0
        self.height_of_current_block = 0
        
        if util.get_debug():
            self.debug()