import beliefTable


class Node(object):
    def __init__(self, name, table, parents=None):
        # name = a string
        # table = a belief table
        # parents = a list of Nodes
        self.name = name
        self.table = table
        if parents == None:
            self.parents = []
        else:
            self.parents = parents
        self.children = []


class BayesianNetwork(object):

    def __init__(self, name, nodes=None):
        # nodes = a list of Nodes
        self.name = name
        if nodes == None:
            self.nodes = []
        else:
            self.nodes = nodes
        self.evidences = []

    def addNode(self, name, table, parents=None):
        # name = a string
        # table = a belief table
        # parents = a list of strings (name of the parents)
        if len(self.nodes) == 0 and parents == None:
            self.nodes.append(Node(name=name, table=table))
        else:
            if parents == None:
                parents = []
            p = []
            for i in parents:
                for n in self.nodes:
                    if n.name == i:
                        p.append(n)
            if len(p) == len(parents):
                new = Node(name=name, table=table, parents=p)
                for i in p:
                    i.children.append(new)
                self.nodes.append(new)
                return True
        return False

    def setEvidence(self, variables, values):
        # variables: array of names(strings)
        # values: array of booleans
        if len(variables) != len(values):
            return False
        for l in range(len(variables)):
            self.evidences.append([variables[l], values[l]])
        value = iter(values)
        for var in variables:
            v = next(value)
            for node in self.nodes:
                if var == node.name:
                    node.table.putEvidence(variable=var, value=v)
        return True

    def getProbUniverse(self):
        p = self.nodes[0].table
        for i in range(1, len(self.nodes)):
            p = beliefTable.multiplyBTs(p, self.nodes[i].table)
        return p

    def getProb(self, variables):
        universe = self.getProbUniverse()
        prob = []
        for i in range(len(variables)):
            prob.append(beliefTable.marginalize(universe, variables[i]))
            div = prob[i].table[0][0] + prob[i].table[0][1]
            for j in range(2):
                prob[i].table[0][j] /= div
        return prob


def getBN(name):
    bn = BayesianNetwork(name)
    bts = beliefTable.modelBTs(name)
    if name == 'asia':
        bn.addNode(name='asia', table=bts[0])
        bn.addNode(name='tub', table=bts[1], parents=['asia'])
        bn.addNode(name='smoke', table=bts[2])
        bn.addNode(name='lung', table=bts[3], parents=['smoke'])
        bn.addNode(name='bronc', table=bts[4], parents=['smoke'])
        bn.addNode(name='either', table=bts[5], parents=['lung', 'tub'])
        bn.addNode(name='xray', table=bts[6], parents=['either'])
        bn.addNode(name='dysp', table=bts[7], parents=['bronc', 'either'])
    elif name == 'cancer':
        bn.addNode(name='pollution', table=bts[0])
        bn.addNode(name='smoker', table=bts[1])
        bn.addNode(name='cancer', table=bts[2], parents=['smoker', 'pollution'])
        bn.addNode(name='xray', table=bts[3], parents=['cancer'])
        bn.addNode(name='dyspnea', table=bts[4], parents=['cancer'])
    elif name == 'sprinkler':
        bn.addNode(name='cloudy', table=bts[0])
        bn.addNode(name='sprinkler', table=bts[1], parents=['cloudy'])
        bn.addNode(name='rain', table=bts[2], parents=['cloudy'])
        bn.addNode(name='wet_grass', table=bts[3], parents=['sprinkler', 'rain'])
    return bn


model = getBN('asia')
variables = ['asia', 'smoke', 'dysp']
values = [False, True, True]
model.setEvidence(variables, values)

prob = model.getProb(['asia', 'bronc', 'dysp', 'either', 'lung', 'smoke', 'tub', 'xray'])
for p in prob:
    p.print()

model = getBN('cancer')
variables = ['pollution', 'smoker']
values = [False, True]
model.setEvidence(variables,values)

prob = model.getProb(['cancer', 'dyspnea', 'pollution', 'smoker', 'xray'])
for p in prob:
    p.print()

model = getBN('sprinkler')
variables=['cloudy','wet_grass']
values=[True,True]
model.setEvidence(variables,values)

prob = model.getProb(['cloudy','rain','sprinkler','wet_grass'])
for p in prob:
    p.print()
