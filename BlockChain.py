#!/usr/bin/python3

import json
import time
import hashlib
from typing import List

class Block:
    '''
    A block to store data
    
    :attr index: a unique index of the block
    :attr data: data the block stores
    :attr timestamp: time of the block created
    :attr previous_hash: hash of the previous block in blockchain
    :attr nonce: a nonce to make hash 
    '''
    def __init__(self, index, data, previous_hash : str, time_format = '%Y-%m-%d %H:%M:%S'):
        self.index = index
        self.data = data
        self.timestamp = time.strftime(time_format)
        self.previous_hash = previous_hash
        self.nonce = 0
        
    def hash(self):
        return hashlib.sha256(self.dump().encode()).hexdigest()
    
    def dump(self):
        return json.dumps(self.__dict__, sort_keys=True)
        
    
class BlockChain:
    '''
    The blockchain to store blocks
    
    :attr chain: the chain of blocks
    :attr valid_func: the function to restrict block hash
    '''
    def __init__(self, valid_func):
        self.chain : List[Block] = []
        self.valid_func = valid_func
        
    def mine(self, block : Block):
        '''
        Mine a block by tring its nonce.
        
        :param block: the block to be mined
        '''
        while not self.valid_func(block.hash()):
            block.nonce += 1
        
    def addBlock(self, block : Block) -> bool:
        '''
        Add a block to the chain.
        
        :param block: the new mined block
        :return: true if added successfully
        '''
        if not self.chain:
            self.chain.append(block)
            return True
        
        hash_value = block.hash()
        if not self.valid_func(hash_value):
            return False
        if not block.previous_hash == self.chain[-1].hash():
            return False
        
        self.chain.append(block)
        return True
        
    def lastHash(self):
        if not self.chain:
            return None
        return self.chain[-1].hash()
        
    def checkValid(self) -> bool:
        '''
        Check whether the blockchain is valid.
        '''
        previous_hash = None
        
        for i in range(len(self.chain)):
            new_hash = self.chain[i].hash()
            if i > 0:
                if not self.chain[i].previous_hash == previous_hash:
                    return False
            if not self.valid_func(new_hash):
                return False
            previous_hash = new_hash
            
        return True
    
    @staticmethod
    def ValidFunc_StartsWith0s(num):
        return lambda hash_value: True if hash_value.startswith('0' * num) else False
    
if __name__ == "__main__":
    blockchain = BlockChain(BlockChain.ValidFunc_StartsWith0s(2))
    
    block1 = Block(0, "Hello world, 你好", blockchain.lastHash())
    blockchain.mine(block1)
    print(block1.dump())
    print(block1.hash())
    blockchain.addBlock(block1)
    
    block2 = Block(1, "awsl!", blockchain.lastHash())
    blockchain.mine(block2)
    print(block2.dump())
    print(block2.hash())
    result = blockchain.addBlock(block2)
    
    print(result)
    