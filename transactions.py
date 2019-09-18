import hashlib as hsh
import datetime as dt
import math
import tree

import multiprocessing

debug = 1

class trrecord:
    def __init__(self, source, dest, transfer, amnt, timestamp, lastHash):
        self.source = str(source)
        self.dest = str(dest)
        self.transfer = str(transfer) #interim transfer account ID
        self.amnt = str(amnt)
        self.timestamp = str(timestamp)
        self.lastHash = lastHash

    def currentHash(self):
        self.hash = str(self.source) + str(self.dest) + str(self.transfer) + str(self.amnt) + str(self.timestamp) + str(self.lastHash)
        self.hash = hsh.sha256(self.hash.encode()).hexdigest()
        return self.hash
            
        


class block():
    def __init__(self, lastHash, addr, key, n_of_levels=4, difficulty = 2):
        self.addr = addr

        self.extraNonce = trrecord('0000', '0000', '0000', '0000', dt.datetime.utcnow(), 0)
        self.nonce = 0
        self.transactions = [self.extraNonce]
        self.merkle = tree.tree([0,0])
        self.hash = ''
        self.lastHash = lastHash
        self.key = key
        self.trnbuffer = []
        self.capacity = 2**n_of_levels
        self.commitflag = 0
        self.difficulty = difficulty

        # propogate the merkle tree w/ 31 empty nodes, such that
        # each block will have space for 16 transactions

        for i in range(0, n_of_levels):
            self.merkle.insert_level()
        
    def ins_transaction(self, trn):
        global debug
        if len(self.trnbuffer) == self.capacity:
            return 0
        elif len(self.trnbuffer) == self.capacity-1:
            self.commitflag = 1
        if len(self.trnbuffer) != 0:
            trn.lastHash = str(self.trnbuffer[len(self.trnbuffer)-1].source)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].dest)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].transfer)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].amnt)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].timestamp)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].lastHash)
            trn.lastHash += str(self.trnbuffer[len(self.trnbuffer)-1].currentHash())
            trn.lastHash = hsh.sha256(trn.lastHash.encode()).hexdigest()
        else:
            trn.lastHash = 0
        self.trnbuffer.append(trn)


        if self.commitflag:
            if input("Last transaction in sequence. Commit and work? (y to continue, anything else to abort)").lower() == 'y' :
                for i in range (0, len(self.trnbuffer)):
                    self.merkle.findnode([self.merkle.leaf_level(), i]).data = self.trnbuffer[i]
                    if i == 0:
                        self.merkle.findnode([self.merkle.leaf_level(), 0]).data.lastHash = 0
                    else:
                        self.merkle.findnode([self.merkle.leaf_level(), i]).data.lastHash = self.merkle.findnode([self.merkle.leaf_level(), i-1]).data.currentHash()
                self.hashTree()
                if debug == 1:
                    print("Will now work block")
                self.work()
                return 1

        else: return 1

    def hashTree(self):

        cur_level = self.merkle.leaf_level()-1

        for x in range(0, self.merkle.leaf_level()-1):
            
            cur_level_nodes = 2**cur_level

            for i in range(0, cur_level_nodes):

                if cur_level == self.merkle.leaf_level()-1:
                    cursor = self.merkle.findnode([cur_level, i])
                    tohash = str(cursor.left.addr) + str(cursor.left.data.source) + str(cursor.left.data.dest) + str(cursor.left.data.transfer) + str(cursor.left.data.amnt) + str(cursor.left.data.timestamp) + str(cursor.left.data.lastHash)
                    tohash += tohash + str(cursor.right.addr) + str(cursor.right.data.source) + str(cursor.right.data.dest) + str(cursor.right.data.transfer) + str(cursor.right.data.amnt) + str(cursor.right.data.timestamp) + str(cursor.right.data.lastHash)
                    cursor.data = hsh.sha256(tohash.encode()).hexdigest()
                else:
                    cursor = self.merkle.findnode([cur_level, i])
                    cursor.data = hsh.sha256((cursor.right.data + cursor.left.data).encode()).hexdigest()

            cur_level -= 1

    def work(self):
        while (self.nonce <= 10**100):
            tohash = self.merkle.left.data + self.merkle.right.data + str(self.nonce)
            self.hash = hsh.sha256(tohash.encode()).hexdigest()
            if (self.hash[0:self.difficulty] == '0' * self.difficulty):
                return 1
            else:
                self.nonce +=1

        self.merkle.findnode([self.merkle.leaf_level(), 0]).data.lastHash +=1
        if(debug == 1):
            print("Extranonce incremented by 1")
        self.work()

def trn_test(difficulty):
    testblock = block(0, 0, 0, difficulty=difficulty)
    testtrns = []
    print("Created a block!")
    for i in range(0, 16):
        ctrn = trrecord(i, i*4, i**1, 2**i*2, dt.datetime.utcnow(), 0)
        testtrns.append(ctrn)
    print("Pulled some transactions out of thin air!")
    for i in testtrns:
        testblock.ins_transaction(i)
    print ("Inserted transactions!")
    return testblock