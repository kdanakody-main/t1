class tree:
    def __init__(self, addr, data = None):
        self.left, self.right = None, None
        self.data = data
        self.addr = addr

    # def singleInsertCheck(self, data, cursor): #not in use
    #     # cursor = self
    #     if cursor.left == None:
    #         cursor.left = tree([self.addr[0]+1,self.addr[1]*2])
    #         cursor = cursor.left
    #         cursor.data = data
    #         return cursor
    #     elif cursor.right == None:
    #         cursor.right = tree([self.addr[0]+1, (self.addr[1]*2)+1])
    #         cursor = cursor.right
    #         cursor.data = data
    #         return cursor
    #     else: return 0
        
    # def insert_v1(self, data): #not in use
    #     #cursor = cursor.move_up()
    #     cursor = self
    #     while 1:
    #         if self.singleInsertCheck(data, cursor):
    #             break
    #         elif self.singleInsertCheck(data, cursor.left):
    #             break
    #         elif self.singleInsertCheck(data, cursor.right):
    #             break
    '''                 Mostly deprecated function- insert_level() is preferred
    def insert(self, data):
        level = 0
        insert_parent = 0
        while 1:
            for i in range(0, (2**(level+1))):
                if not self.findnode([level+1, i]):
                    #figure out parent node, then if left or right
                    #step1: parent node
                    insert_parent = self.parent([level+1, i])
                    if i%2 == 0:
                        insert_parent.left = tree([level+1, i], data)
                    else:
                        insert_parent.right = tree([level+1, i], data)
                    return self.findnode([level+1, i])
                else:
                    pass
            level += 1
            '''

    def insert_level(self):
        ll = self.leaf_level()
        il = ll + 1
        n_elements = 2**il
        cur_addr = [0,0]
        for i in range (0, n_elements):
            cur_addr = [il, i]
            cur_addr_parent = self.parent(cur_addr)
            if i%2 == 0:
                cur_addr_parent.left = tree(cur_addr)
            else:
                cur_addr_parent.right = tree(cur_addr)

    def leaf_level(self): #most recent level of leaves
        n = 0
        cursor = self
        while cursor.left:
            cursor = cursor.left
            n += 1
        return n
    def nodes_level(self, level):
        if self.findnode([level, 0]):
            cursor = self.findnode([level, 0])
        else:
            return 0
        n = 1
        while self.findnode([level, cursor.addr[1]+1]):
            cursor = self.findnode([level, cursor.addr[1]+1])
            n += 1
        return n

    def size(self): #total number of nodes in the tree
        level = 0
        n_nodes = 0
        while 1:
            for i in range(0, (2**(level))):
                if self.findnode([level, i]):
                    n_nodes +=1
                else:
                    return n_nodes
            level += 1

    # def move_up(self):
    #     return self.findnode([self.addr[0]-1, self.addr[1]//2]) #deprecated

    def parent(self, node): #node is a node address [level, nodenumber]
        return self.findnode([node[0]-1, node[1]//2])

    def findnode(self, node):
        #node address will be in the form of tuple (level, number)
        levels_below_root = node[0] - self.addr[0]
        cursor = self
        workingaddress = node.copy()
        if node == [0,0]:
            return self
        while cursor.addr != node:
            nodes_to_split = 2**levels_below_root
            if workingaddress[1] < ((nodes_to_split/2)):
                if cursor.left:
                    cursor = cursor.left
                else: return None
            else:
                if cursor.right:
                    cursor = cursor.right
                else: return None
            levels_below_root = node[0] - cursor.addr[0]
            workingaddress[1] = workingaddress[1]%(nodes_to_split/2)

        return cursor