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

class TreeNode:
    def __init__(self, leaves = None, parent=None):
        self.leaves = leaves
        self.rightChild = None
        self.leftChild = None
        self.parent = parent
        self.query = None
    
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
        s = ""
        s += f"query: {self.query[0]} == {self.query[1]}\n"
        s+="false: {\n"
        s+=str(self.leftChild)
        s+="\n}\ntrue: {\n"
        s+=str(self.rightChild)
        s+="\n}\n"

        return s
        
root = TreeNode(leaves=data)
root.greedyConstruct([0 for _ in queries])

print(root)