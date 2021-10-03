class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis
        self.H1 = {
            'A': 1,
            'B': 6,
            'C': 2,
            'D': 2,
            'E': 2,
            'F': 1,
            'G': 5,
            'H': 7,
            'I': 7,
            'J': 1,
            'T': 3
        }
        
        self.H = {
            'A': 1,
            'B': 6,
            'C': 12,
            'D': 10,
            'E': 4,
            'F': 4,
            'G': 5,
            'H': 7,
            
            
        }
        self.parent={}
        self.openList=set()
        self.hasRevised=[]
        self.solutionGraph={}
        self.solvedNodeList=set()
 
    def get_neighbors(self, v):
        return self.adjac_lis.get(v,'')
    
    def updateNode(self, v):
    
        if v in self.solvedNodeList:
            return
                  
        
        feasibleChildNodeList=[]
        minimumCost=None
        minimumCostFeasibleChildNodesDict={}
        
        print("CURRENT PROCESSING NODE:", v)
        print("___________________________")
        
        #computing the minimum cost by visiting all child nodes with "OR/AND" condition
        for (c, weight) in self.get_neighbors(v):
          
            feasibleChildNodeList=[]    #initialize for computing any new feasibileChildNodes(childnodes with minimum cost)
           
            cost= self.getHeuristicNodeValue(c) + 1   # assuming all the edges with equal weight one
            feasibleChildNodeList.append(c)
            andNodesList=self.getAndNodes(v)
            
            for nodeTuple in andNodesList:  #checking whether the child(c) is in "AND" condition with other nodes
                if c in nodeTuple:
                    for andNode in nodeTuple:
                        if andNode!=c:
                            feasibleChildNodeList.append(andNode)
                            cost=cost+self.getHeuristicNodeValue(andNode) + 1  #compute total cost of "AND" nodes
           
                    
            if minimumCost==None: #inializing minimum cost 
                minimumCost=cost
                for child in feasibleChildNodeList:            #capturing parent child relationship
                    self.parent[child]=v                               
                minimumCostFeasibleChildNodesDict[minimumCost]=feasibleChildNodeList    #mapping minimum cost child nodes          
                
                
            else:
                if minimumCost>cost:       #checking minimum cost child nodes 
                    minimumCost=cost
                    for child in feasibleChildNodeList:
                        self.parent[child]=v
                    minimumCostFeasibleChildNodesDict[minimumCost]=feasibleChildNodeList
            
                    
                
        if minimumCost==None:                                 # no child nodes of the give node v and mark as solved node
            minimumCost=self.getHeuristicNodeValue(v)        
            self.solvedNodeList.add(v)
            
        else:
            self.setHeuristicNodeValue(v,minimumCost)         # minimum cost found! assign to the given node v  
            for child in minimumCostFeasibleChildNodesDict[minimumCost]:
                if child not in self.solvedNodeList:          # checking whether minimum cost child nodes are solved 
                    self.openList.add(child)                  # if not solved add node/s to openList for exploration
            self.solutionGraph[v]= minimumCostFeasibleChildNodesDict[minimumCost]
                                                              # capture minimum cost child nodes as part of graph solution
            
        solved=True
        for c in self.solutionGraph.get(v,''):                # checking if feasible minimum cost child nodes are already solved
            if c not in self.solvedNodeList:                   
                solved=solved & False
                
        if solved == True:                                   # if all the feasible child nodes of the given node are solved
            self.solvedNodeList.add(v)                       # mark the given node v as solved
                         
            
        print("HEURISTIC VALUES  :", self.H)
        print("OPEN LIST         :", list(self.openList))
        print("MINIMUM COST NODES:", minimumCostFeasibleChildNodesDict.get(minimumCost,"[ ]"))
        print("SOLVED NODE LIST  :", list(self.solvedNodeList))
        print("-----------------------------------------------------------------------------------------")     
        
    
    def getAndNodes(self,v):
        andNodes={
            # PARENT NODE AS KEY FOR ITS CHILD NODES IN AND CONDITION
            'A':[('B','C')],
            'D':[('E','F')]
        }
        
        return andNodes.get(v, '')
    
    def getHeuristicNodeValue(self, n):
        return self.H.get(n,0)  #Always return the heuristic value
 
    def setHeuristicNodeValue(self, n, value):
        self.H[n]=value        # sets the revised heuristic value of a give node 

    def ao_star_algorithm(self, start):
        # In this open_lst is a list of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start node.
        # And closedList is a list of nodes which have been visited and who's neighbors have been always inspected.
        self.openList = set([start])
      
        while len(self.openList) > 0:
        
            # it will find a node with the lowest value of f() -
            v = self.openList.pop()       # procesess a Node in the openList
            
            self.updateNode(v)
                
            while v!=start and self.parent[v] not in self.solvedNodeList:
                
                parent=self.parent[v];
                self.updateNode(parent)
                v=parent
            
            print("TRAVERSE SOLUTION FROM ROOT TO COMPUTE THE FINAL SOLUTION GRAPH")
            print("---------------------------------------------------------------")
            print("SOLUTION GRAPH:",self.solutionGraph)
            print("\n")
                                         
nodeList1 = {
    'A': [('B', 1), ('C', 1), ('D', 1)],
    'B': [('G', 1), ('H', 1)],
    'C': [('J', 1)],
    'D': [('E', 1), ('F', 1)],
    'G': [('I', 1)]
    
}

nodeList = {
    'A': [('B', 1), ('C', 1), ('D', 1)],
    'B': [('G', 1), ('H', 1)],
    'D': [('E', 1), ('F', 1)]
    
    
}
graph = Graph(nodeList)
graph.ao_star_algorithm('A') 
