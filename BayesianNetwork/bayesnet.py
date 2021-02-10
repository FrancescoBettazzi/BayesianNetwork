class Node(object):
    def __init__(self, name, table, father=None):
        # name = a string
        # table = a belief table
        # father = a Node
        self.name = name
        self.table = table
        self.father = father
        self.children = None


class BayesianNetwork(object):

    def __init__(self, nodes=None):
        # nodes = a list of Nodes
        self.nodes = nodes

    def addNode(self, name, table, father=None):
        # name = a string
        # table = a belief table
        # father = a string (name of the father)
        f = None
        for n in self.nodes:
            if n.name == name:
                print('Nome già presente')
                return False
            if n.name == father:
                f = n
        if father != None and f == None:
            print('Padre non presente')
            return False
        new = Node(name=name, table=table, father=f)
        f.children.append(new)
        self.nodes.append(new)
