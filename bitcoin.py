#!/usr/bin/env python
import os
import sys
import multiprocessing 
import Node
import util
import time

if __name__ == "__main__":

    node_cnt = int(sys.argv[1])
    
    if util.get_debug():
        print("# number of nodes :",node_cnt)

    '''
    Creating a shared memory for each process to communicate between each other. 
    Source https://www.youtube.com/watch?v=sp7EhjLkFY4
    '''

    q_list = []
    for i in range(node_cnt):
        q_list.append(multiprocessing.Queue())
    
    if util.get_debug():
        print("# queue_list :",q_list)
    
    # number of zeros in proof of work and leaf size for merkel tree
    pow_zeros = int(sys.argv[2])
    leaf_sz = int(sys.argv[3])
    
    if util.get_debug():
        print("# Proof of work Zeros :",pow_zeros)
        print("# leaf size :",leaf_sz)
    
    # creating common list for all the nodes
    common_list = multiprocessing.Manager().list()
    
    # Creating nodes for the bitcoin
    nodes = []
    message_limit = 3
    for i in range(node_cnt):
        nodes.append(Node.Node(i,node_cnt,pow_zeros,leaf_sz,common_list,message_limit))
        
    # creating multi-threads using the following funtion
    node_process = []
    for i in range(node_cnt):
        process = multiprocessing.Process(target=nodes[i].run_node,args = (q_list,))
        node_process.append(process)
        
    # Running the process
    for i in node_process:
        i.start()
    
    for i in node_process:
        i.join()
    