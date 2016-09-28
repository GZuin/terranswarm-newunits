import random


terminals = ['int','float','Unit-Gas','Unit-Mineral','Current-Gas',
			 'Current-Mineral','Time','TotalUnits','NumUnits',
			 'NumBases','NumSVC']
			 
operators = ['IF','AND',
			'+','-','*','/','^',
			'>','<','>=','<=','==','!']
			
			
growTree(T,node,termProb):
	nextLeftNode=''
	nextRightNode=''
	i = random.uniform(0.0,1.0)
	if(node=='IF' or node=='AND'):
		if(termProb>=i):
			nextNode
		else:
	
	