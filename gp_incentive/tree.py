import random
import os
import sys

ifs = []

'''terminals = ['int','float',
			'Unit-Gas','Unit-Mineral','Current-Gas',
			'Current-Mineral','Time','TotalUnits','NumThisUnits',
			'NumBases','NumSVC']							# possible terminals. Upper case means its derived from SC current state
'''
terminals = ['int','float','x','y','z']
# float is a percentage [-1.0 , 1.0] // int is a value [-9999 , 9999]

condoperands = ['>','<','>=','<=','==']                         # conditonal operands. Only usable as 'IF' middle child
adcdoperands = ['!','&&','||']                                  # aditional control operands
commoperands = ['+','-','*','/']			        # common operands, can be used anywhere
ctrloperands = ['IF']						# program flux control operands

 
'''operands = 	['IF','AND',
			'+','-','*','/','^',
			'>','<','>=','<=','==','!']
'''
nodeNumber = 0


class Tree():
    def __init__(self,value):
        self.left = None
	self.right = None
	self.middle = None
        self.father = None
	self.insideif = False
	self.pflag = False
        self.depth = 1
        self.height = 1
        if (value == 'int'):
            self.value = str(random.randint(-9999,9999))
        elif (value == 'float'):
            self.value = str(random.uniform(-1.0,1.0))
        else:
            self.value = value

    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
    def getMiddleChild(self):
	return self.middle
    def setNodeValue(self,value):
        self.value = value
    def getNodeValue(self):
        return self.value
    def getFather(self):
        return self.father
    def getPrinted(self):
        return self.pflag
    def setPrinted(self):
        self.pflag=not self.pflag

    def insertRight(self,newNode):
        if self.right == None:
            self.right = Tree(newNode)
        else:
            tree = Tree(newNode)
            tree.right = self.right
            self.right = tree
    	#self.right.insideif = self.insideif
        self.right.father = self
        self.right.depth = self.depth+1
        self.updateHeight(self,self.right.height+1)

    def insertMiddle(self,newNode):
        if self.middle == None:
            self.middle = Tree(newNode)
        else:
            tree = Tree(newNode)
            tree.middle = self.middle
            self.middle = tree
	#self.middle.insideif = True
        self.middle.father = self
        self.middle.depth = self.depth+1
        self.updateHeight(self,self.middle.height+1)
		

    def insertLeft(self,newNode):
        if self.left == None:
            self.left = Tree(newNode)
        else:
            tree = BinaryTree(newNode)
            self.left = tree
            tree.left = self.left
	#self.left.insideif = self.insideif
        self.left.father = self
        self.left.depth = self.depth+1
        self.updateHeight(self,self.left.height+1)

    def updateHeight(self,node, newheight):
        if(newheight > node.height):
            node.height = newheight
            if(node.father != None):
                node.updateHeight(node.father, newheight + 1)

def printTree(node): #outdated
    s = ""
    for i in range(1,node.depth):
        s = s + "\t"
    print(s+str(node.value))
    if(node.middle != None):
        printTree(node.middle)
    if(node.left != None):
        printTree(node.left)
    if(node.right != None):
        printTree(node.right)
    return


def printCTree(node): #outdated
    s = ""
    for i in range(1,node.depth):
        s = s + "\t"
    print(s+str(node.value))
    if(node.middle != None):
        printTree(node.middle)
    if(node.left != None):
        runandprintC(node.left)
    if(node.right != None):
        runandprintC(node.right)
    return

ifcounter = 0

def printNode(Node):
    global ifcounter
    s=""
    #for i in range(1,Node.depth):
    #    s = s + "\t"
    if Node.getLeftChild()==None:
        sys.stdout.write(s+Node.getNodeValue())
        Node.setPrinted()
        return
    if Node.value=='IF':
        this_if = ifcounter
        ifcounter+=1
        #print "float "+Node.value+str(this_if)+'=0'
        #sys.stdout.write(s+Node.value + '(')
        Node.setPrinted()
        sys.stdout.write('(')
        printNode(Node.middle)
        #sys.stdout.write('){\nreturn ')
        sys.stdout.write(' ? ')
        printNode(Node.left)
        #sys.stdout.write('}\nelse{\nreturn
        sys.stdout.write(' : ')
        printNode(Node.right)
        #sys.stdout.write( '}\n')
        sys.stdout.write(')')
        return
    
    sys.stdout.write('(')
    printNode(Node.left)
    sys.stdout.write(s+Node.getNodeValue())
    printNode(Node.right)
    sys.stdout.write(')')
    return
        
    
def iterate(node):
    Node = getFirst(node)
    while (Node!=None):
        if Node.getNodeValue()=='IF':
            Node.setNodeValue('IF'+str(len(ifs)))
            ifs.append(Node.getMiddleChild())
        Node = getNext(Node)

def runandprintC(node):
    Node = getFirst(node)
    while (Node!=None):
        print (Node.getNodeValue())
        Node = getNext(Node)

def oldprintTreeC(node):
    iterate(node)
    runandprintC(node)

def getLeftMost(Node):
    n = Node
    while(n.getLeftChild() != None):
        n=n.getLeftChild()
    return n

def getFirst(Tree):
    return getLeftMost(Tree)


def getNext(Node):
    n = Node
    if(n.getRightChild() != None):
        return getLeftMost(n.getRightChild())
    else:
        while(n.getFather() != None and n == n.getFather().getRightChild()):
            n=n.getFather()
    return n.getFather()    


#TODO: FIX THIS TO NEW TREE KIND
def growTree(Node,operatorProb,maxdepth):

    #Left Side
    i = random.uniform(0.0,1.0)

    if (i <= operatorProb and Node.depth<maxdepth):
	if Node.insideif == True:
		op=random.choice(condoperands+commoperands+ctrloperands+adcdoperands)
		while (op=='IF' and Node.depth>maxdepth-2): #avoid IFs that wont have enough space to grow
			op=random.choice(condoperands+commoperands+ctrloperands)
	else:
		op=random.choice(commoperands+ctrloperands)
		while (op=='IF' and Node.depth>maxdepth-2): #avoid IFs that wont have enough space to grow
				op=random.choice(commoperands+ctrloperands)
	Node.insertLeft(op)
        growTree(Node.left,operatorProb,maxdepth)
    else:
        Node.insertLeft(random.choice(terminals))
        Node.left.left = None
        Node.left.right = None


	#Middle Side
    if(Node.value=='IF'):
	Node.insertMiddle(random.choice(condoperands))
	growTree(Node.middle,operatorProb,maxdepth)
		
    #Right Side
    i = random.uniform(0.0,1.0)

    if (i <= operatorProb and Node.depth<maxdepth):
	if Node.insideif == True:
		op=random.choice(condoperands+commoperands+ctrloperands+adcdoperands)
		while (op=='IF' and Node.depth>maxdepth-2): #avoid IFs that wont have enough space to grow
			op=random.choice(condoperands+commoperands+ctrloperands)
	else:
		op=random.choice(commoperands+ctrloperands)
		while (op=='IF' and Node.depth>maxdepth-2): #avoid IFs that wont have enough space to grow
			op=random.choice(commoperands+ctrloperands)
	Node.insertRight(op)
        growTree(Node.right,operatorProb,maxdepth)
    else:
        Node.insertRight(random.choice(terminals))
        Node.right.left = None
        Node.right.right = None

def generateTreeFromFile(ifile):    
    value = ifile.readline()
    value = value[:-1]

    if (value=="+" or value=="-" or value=="*" or value=="/" or value=="exp"):
        Tree = BinaryTree(value)
    else:
        Tree = BinaryTree(value)
        return Tree

    growFromFile(Tree,Tree,ifile)
    return Tree

def growFromFile(Root,Node,ifile):

    #Left Side
    value = ifile.readline()
    value = value[:-1]

    if (value=="+" or value=="-" or value=="*" or value=="/" or value=="exp"):
        Node.insertLeft(value)
        growFromFile(Root,Node.left,ifile)
    else:
        Node.insertLeft(value)
        Node.left.left = None
        Node.left.right = None

    #Right Side
    value = ifile.readline()
    value = value[:-1]

    if (value=="+" or value=="-" or value=="*" or value=="/" or value=="exp"):
        Node.insertRight(value)
        growFromFile(Root,Node.right,ifile)
    else:
        Node.insertRight(value)
        Node.right.left = None
        Node.right.right = None

if __name__ == '__main__':
	t = Tree('IF')
	growTree(t,0.7,4)
	printTree(t)
	print('------------------')
        printNode(t)
