#!/usr/bin/env python

#Importing necessary modules
import hashlib
from Crypto.PublicKey import RSA
from binascii import hexlify
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

def create_hash(s):
    uni = s.encode()
    hash_object = hashlib.sha256(uni)
    hex_dig = hash_object.hexdigest()
    if get_debug():
        print(hex_dig)
    return(hex_dig)

def RSA_to_key(key):
    return RSA.importKey(key)

def public_private_key():
    rng = Random.new().read
    #Generating private key (RsaKey object) of key length of 1024 bits
    private_key = RSA.generate(1024, rng)
    #Generating the public key (RsaKey object) from the private key
    public_key = private_key.publickey()
    
    if get_debug():
        print("# Type of private key and public key")
        print("# ",type(private_key), type(public_key))
    
    '''It prints the following output.
    <class ‘Crypto.PublicKey.RSA.RsaKey’>
    <class‘Crypto.PublicKey.RSA.RsaKey’>
    '''
    
    '''
    Now, the private_key is ‘RsaKey’ object. From it, we can create a 
    corresponding public key using the method ‘publickey()’ on the 
    ‘RsaKey’ private_key object.
    '''
    
    
    #Converting the RsaKey (binary data) objects to string 
    #private_pem = private_key.export_key().decode()
    private_pem = private_key.export_key()
    #public_pem = public_key.export_key().decode()
    public_pem = public_key.export_key()
    
    if get_debug():
        print("# Type of private pem and public pem")
        print("# ",type(private_pem), type(public_pem))
        print("# Private pem and public pem")
        print("# ",private_pem,public_pem)
    
    # return binary private and public key
    return (private_pem, public_pem)

# to sign a message. here pri_key is in bytes
def sign_message(message,pri_key):
    signer = PKCS1_v1_5.new(pri_key)
    d = SHA256.new()
    d.update(message.encode())
    sig = signer.sign(d)
    
    if get_debug():
        print(sig.hex())
    
    return sig
    
# to verify the signed message
def verify_message(message,sign,pub_key):
    message_digest = SHA256.new()
    message_digest.update(message.encode())
    verifier = PKCS1_v1_5.new(pub_key)
    verified = verifier.verify(message_digest, sign)
    return verified


# creating a merkle tree
def create_merkle_tree(tot_leaves,leaf_sz):
    leaves = tot_leaves
    len_leaves = len(leaves)
    
    if get_debug():
        print("# total number of leaves :",len_leaves)
        print("# leaves :",leaves)
    
    '''
    Check if leaves are in order of leaf_sz if not then replicate the last
    value of the leaves and make the number of leaves as the multiple of leaf_sz
    '''

    if len_leaves % leaf_sz != 0 :
        # number of extra leaves to add to make it multiple of leaf_sz.
        leaves_to_add = leaf_sz - (len_leaves % leaf_sz)
        
        # final length of len_leaves will be.
        len_leaves +=leaves_to_add
        
        # adding the leaves.
        for i in range(leaves_to_add):
            leaves.append(leaves[-1])

    if get_debug():
        print("# New leaves :",leaves)
    
    merkle_tree = [leaves]
    
    while(len_leaves != 1):
        temp = merkle_tree[-1]
        
        cnt =0
        
        pair_leaves = []
        for i in range(len(temp)//leaf_sz):
            temp1 = []
            for j in range(leaf_sz):
                temp1.append(temp[cnt])
                cnt+=1
            pair_leaves.append(temp1)
        
        if get_debug():
            print("# pair_leaves :",pair_leaves)
        
        leaves = []
        
        for i in range(len(pair_leaves)):
            str_data = ""
            for j in pair_leaves[i]:
                str_data = str_data+str(j)
            leaves.append(create_hash(str_data))
            
        
        len_leaves = len(leaves)
        if get_debug():
            print("# total number of leaves :",len_leaves)
            print("# leaves :",leaves)
        
        if len_leaves % leaf_sz != 0  and len_leaves != 1:
            # number of extra leaves to add to make it multiple of leaf_sz.
            leaves_to_add = leaf_sz - (len_leaves % leaf_sz)
        
            # final length of len_leaves will be.
            len_leaves +=leaves_to_add
        
            # adding the leaves.
            for i in range(leaves_to_add):
                leaves.append(leaves[-1])
        merkle_tree.append(leaves)
                
    return merkle_tree


#########################################################
######## Setting for the code ###########################
#########################################################

# Initial amount for all the nodes
def get_initial_amount():
    return 5000

# Block creation reward
def get_block_create_reward():
    return 5

# Block creation time
def get_block_create_time():
    return 20

# Transaction charges
def get_transaction_charges():
    return 2

# For smart contract
def get_smart_contract():
    return True

def get_smart_contract_nodes():
    dict_nodes  = {}
    dict_nodes[0] = 1
    return dict_nodes

def get_smart_contract_balance():
    return 3000

# Max time for which each node will run
def get_total_time():
    return 10


# for debuging and printing logs of the program
def print_logs():
    return True
def get_debug():
    return True


'''
if _debug_:
    # here the keys are in binary
    private_k,public_k=public_private_key()
    k = (sign_message("hello world",RSA_to_key(private_k)))
    print(verify_message("hello world",k,RSA_to_key(public_k)))
    
    print(create_merkle_tree(['1','1','2','3','5','6','7','9','10','11','13','15','19'],4))
    
'''
