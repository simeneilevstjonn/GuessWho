import pandas as pd

data = pd.read_csv("characters.csv")

queries = set()

for name, col in data.iteritems():
    if name != "name":
        for val in col.values:
            queries.add((name, val))

# Make list for easier indexing
queries = list(queries)

def greedyChooseBestQuery(nodes, usedQueries):
    bestQuery = None
    bestDiff = float("inf")

    for i, (id, val) in enumerate(queries):
        if not usedQueries[i]:
            t = nodes.loc[lambda x : x[id] == val]
            f = nodes.loc[lambda x : x[id] != val]

            d = abs(len(t) - len(f))

            if d < bestDiff:
                bestDiff = d
                bestQuery = i
    
    return bestQuery

parents = []
children = []
weights = []

nextid = 1

class TreeNode:
    def __init__(self, leaves = None, parent=None):
        self.leaves = leaves
        self.rightChild = None
        self.leftChild = None
        self.parent = parent
        self.query = None
        self.id = -1
    
    def greedyConstruct(self, usedQueries):
        qidx = greedyChooseBestQuery(self.leaves, usedQueries)
        self.query = queries[qidx]
        id, val = queries[qidx]

        uq = usedQueries[::]
        uq[qidx] = True

        t = self.leaves.loc[lambda x : x[id] == val]
        f = self.leaves.loc[lambda x : x[id] != val]

        # At bottom left
        if len(f) == 1:
            self.leftChild = f.iloc[0]["name"]
        else:
            self.leftChild = TreeNode(leaves = f, parent = self)
            self.leftChild.greedyConstruct(uq)
        
        # At bottom right
        if len(t) == 1:
            self.rightChild = t.iloc[0]["name"]
        else:
            self.rightChild = TreeNode(leaves = t, parent = self)
            self.rightChild.greedyConstruct(uq)

    def __str__(self) -> str:
        return f"{self.id}:{self.query[0]}=={self.query[1]}"

    def addToLists(self):
        # Give ids to children
        # If left not string
        global nextid
        if type(self.leftChild) != type(""):
            self.leftChild.id = nextid
            nextid += 1
            self.leftChild.addToLists()
        if type(self.rightChild) != type(""):
            self.rightChild.id = nextid
            nextid += 1
            self.rightChild.addToLists()

        if self.leftChild != None:
            parents.append(str(self))
            children.append(str(self.leftChild))
            weights.append(0)
        if self.rightChild != None:
            parents.append(str(self))
            children.append(str(self.rightChild))
            weights.append(1)     



        
root = TreeNode(leaves=data)
root.greedyConstruct([0 for _ in queries])

root.id = 0

root.addToLists()

if False:
    print(parents)
    print(children)
    print(weights)

def interactive():
    active = root
    while type(active) != type(""):
        print(f"{active.query[0]}=={active.query[1]} y/n?")
        ans = None
        while ans == None:
            raw = input()
            if raw.lower() in ["false","f","n","no"]:
                ans = False
            elif raw.lower() in ["true","t","y","yes"]:
                ans = True
        
        active = active.rightChild if ans else active.leftChild
    
    print(active)

interactive()