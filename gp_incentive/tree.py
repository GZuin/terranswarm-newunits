import random
import os
import shutil
import sys
import subprocess


ifs = []

'''terminals = ['int','float',
			'Unit-Gas','Unit-Mineral','Current-Gas',
			'Current-Mineral','Time','TotalUnits','NumThisUnits',
			'NumBases','NumSVC']							# possible terminals. Upper case means its derived from SC current state
'''
terminals = ['int','float','a','b','c','d','e','f','g','h','i']
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


def writeDefaultText(Outdll,dllname,mode):
    if mode=='Pre':
        Outdll.write("#include \"%s.h\"\n\nfloat DLL_EXPORT incentiveExp(float a, float b, float c, float d, float e, float f, float g, float h, float i)\n{\n\treturn(" % dllname)
    elif mode=='Pos':
        Outdll.write(");\n}\n\nextern \"C\" DLL_EXPORT BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)\n{\n")
        Outdll.write("    switch (fdwReason)\n    {\n")
        Outdll.write("        case DLL_PROCESS_ATTACH:\n            break;\n")
        Outdll.write("        case DLL_PROCESS_DETACH:\n            break;\n")
        Outdll.write("        case DLL_THREAD_ATTACH:\n            break;\n")
        Outdll.write("        case DLL_THREAD_DETACH:\n            break;\n")
        Outdll.write("    }\n    return TRUE; // succesful\n}")

def printTree(node): 
    s = ""
    #for i in range(1,node.depth):
    #    s = s + "\t"
    print(s+str(node.value))
    if(node.middle != None):
        printTree(node.middle)
    if(node.left != None):
        printTree(node.left)
    if(node.right != None):
        printTree(node.right)
    return

def printTreeToFile(Node,Input): 
    Input.write(str(Node.value)+'\n')
    if(Node.middle != None):
        printTreeToFile(Node.middle,Input)
    if(Node.left != None):
        printTreeToFile(Node.left,Input)
    if(Node.right != None):
        printTreeToFile(Node.right,Input)
    return


def printC(Node):
    s=""
    #for i in range(1,Node.depth):
    #    s = s + "\t"
    if Node.getLeftChild()==None:
        sys.stdout.write(s+Node.getNodeValue())
        Node.setPrinted()
        return
    if Node.value=='IF':
        #print "float "+Node.value+str(this_if)+'=0'
        #sys.stdout.write(s+Node.value + '(')
        Node.setPrinted()
        sys.stdout.write('(')
        printC(Node.middle)
        #sys.stdout.write('){\nreturn ')
        sys.stdout.write(' ? ')
        printC(Node.left)
        #sys.stdout.write('}\nelse{\nreturn
        sys.stdout.write(' : ')
        printC(Node.right)
        #sys.stdout.write( '}\n')
        sys.stdout.write(')')
        return
    
    sys.stdout.write('(')
    printC(Node.left)
    sys.stdout.write(s+Node.getNodeValue())
    printC(Node.right)
    sys.stdout.write(')')
    return

def createCDLL(Tree,cppname,dllpath,dllname):
    shutil.copyfile('defaultheader.h',os.path.join(dllpath,cppname+'.h')) # copy header file, same for all
    Outdll = open(os.path.join(dllpath,cppname+'.cpp'),'w') # open source file, will contain the new function
    writeDefaultText(Outdll,cppname,'Pre')
    printCToFile(Tree,Outdll)
    writeDefaultText(Outdll,cppname,'Pos')
    Outdll.close()
    os.system("cl.exe /D_USRDLL /D_WINDLL %s.cpp /MT /link /DLL /OUT:%s.dll > log" % (os.path.join(dllpath,cppname), os.path.join(dllpath,dllname)))
    #args = '/D_USRDLL /D_WINDLL %s.cpp /MT /link /DLL /OUT:%s.dll' % (os.path.join(dllpath,cppname), os.path.join(dllpath,dllname))
    #subprocess.check_call(['cl.exe', args], stdout=os.devnull, stderr=subprocess.STDOUT)


def printCToFile(Node,Input):
    s=""
    #for i in range(1,Node.depth):
    #    s = s + "\t"
    if Node.getLeftChild()==None:
        Input.write(s+Node.getNodeValue())
        Node.setPrinted()
        return
    if Node.value=='IF':
        #print "float "+Node.value+str(this_if)+'=0'
        #sys.stdout.write(s+Node.value + '(')
        Node.setPrinted()
        Input.write('(')
        printCToFile(Node.middle,Input)
        #sys.stdout.write('){\nreturn ')
        Input.write(' ? ')
        printCToFile(Node.left,Input)
        #sys.stdout.write('}\nelse{\nreturn
        Input.write(' : ')
        printCToFile(Node.right,Input)
        #sys.stdout.write( '}\n')
        Input.write(')')
        return
    
    Input.write('(')
    printCToFile(Node.left,Input)
    Input.write(s+Node.getNodeValue())
    printCToFile(Node.right,Input)
    Input.write(')')
    return

    
def iterate(node):
    Node = getFirst(node)
    while (Node!=None):
        if Node.getNodeValue()=='IF':
            Node.setNodeValue('IF'+str(len(ifs)))
            ifs.append(Node.getMiddleChild())
        Node = getNext(Node)

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
    tree = Tree(value)
    
    if (value in condoperands+adcdoperands+commoperands+ctrloperands):
        growFromFile(tree,tree,ifile)

    return tree

def growFromFile(Root,Node,ifile):

    #Middle Side
    if (Node.value=="IF" and Node.middle == None):
        value = ifile.readline()
        value = value[:-1]
        Node.insertMiddle(value)
        growFromFile(Root,Node.middle,ifile)
        #growFromFile(Root,Node.middle.right,ifile)
        #return

    #Left Side
    value = ifile.readline()
    value = value[:-1]

    if (value in condoperands+adcdoperands+commoperands+ctrloperands):
        Node.insertLeft(value)
        growFromFile(Root,Node.left,ifile)
    else:
        Node.insertLeft(value)
        Node.left.left = None
        Node.left.middle = None
        Node.left.right = None

    #Right Side
    value = ifile.readline()
    value = value[:-1]

    if (value in condoperands+adcdoperands+commoperands+ctrloperands):
        Node.insertRight(value)
        growFromFile(Root,Node.right,ifile)
    else:
        Node.insertRight(value)
        Node.right.left = None
        Node.right.middle = None
        Node.right.right = None

if __name__ == '__main__':
	t = Tree('IF')
	growTree(t,0.7,4)
        '''printTree(t)
        i1 = open('tree.txt','w')
        i2 = open('tree_c.txt','w')
	printTreeToFile(t,i1)
	print('------------------')
        printNodeToFile(t,i2)
        i1.close()
        i2.close()

        newt = generateTreeFromFile(open('tree.txt','r'))
        printTree(newt)
        '''
        createCDLL(t,'dlltest','dllex','incexp')
