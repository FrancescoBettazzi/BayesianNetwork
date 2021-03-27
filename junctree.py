import beliefTable
from random import randint


class Cluster(object):
    def __init__(self, variables, table, neighbours=None, separator=False):
        # variables = a list of strings(name of Cluster)
        # table = a belief table
        # neighbours = a list of Clusters
        # separator = boolean
        self.variables = variables
        self.separator = separator
        if neighbours == None:
            self.neighbours = []
        else:
            self.neighbours = neighbours
        self.table = table
        self.old_table = table
        self.root = False
        self.msg = False  # check if the message has passed

    def setRoot(self):
        self.root = True

    def collect(self):
        receiver = []
        for n in self.neighbours:
            if not n.msg:
                receiver.append(n)
        if len(receiver) == 1 and not self.root:
            self.msg = True
            self.sendMessage(receiver[0])
            receiver[0].collect()

    def distribute(self):
        self.msg = False
        for n in self.neighbours:
            if n.msg:
                self.sendMessage(n)
                n.distribute()

    def sendMessage(self, receiver):
        if receiver.separator:
            receiver.old_table = receiver.table
            tmp_vs = receiver.variables
            for i in range(len(tmp_vs)):
                if tmp_vs[i] == 'cancer1' or tmp_vs[i] == 'cancer2':
                    tmp_vs[i] = 'cancer'
            vs = [x for x in tmp_vs if x in self.table.variables]
            receiver.table = beliefTable.marginalizeMSG(table=self.table, variables=vs)
        else:
            tmp = beliefTable.divideBTs(self.table, self.old_table)
            receiver.table = beliefTable.multiplyBTs(tmp, receiver.table)


class JunctionTree(object):
    def __init__(self, name, clusters=None):
        # clusters = a list of Clusters
        self.name = name
        if clusters == None:
            self.clusters = []
        else:
            self.clusters = clusters
        self.evidences = []

    def addCluster(self, variables, table, neighbours=None, separator=False):
        # variables = a list of strings (name of Cluster)
        # table = a belief table
        # neighbours = a list of lists of strings(representing clusters)
        # separator = boolean
        if neighbours != None:
            ns = []
            for c in self.clusters:
                if c.variables in neighbours:
                    ns.append(c)
        else:
            ns = None
        new = Cluster(variables=variables, table=table, neighbours=ns,
                      separator=separator)
        self.clusters.append(new)
        if ns != None:
            for n in ns:
                n.neighbours.append(new)

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
            for cluster in self.clusters:
                if var in cluster.variables:
                    cluster.table.putEvidence(variable=var, value=v)
        self.collectEvidence()
        self.distributeEvidence()
        return True

    def collectEvidence(self):
        self.clusters[0].setRoot()
        for c in self.clusters:
            if len(c.neighbours) == 1 and not c.root:
                c.collect()

    def distributeEvidence(self):
        for c in self.clusters:
            if c.root:
                c.distribute()
                c.root = False

    def getProb(self, variables):
        prob = []
        for v in variables:
            for c in self.clusters:
                if v in c.variables:
                    prob.append(beliefTable.marginalize(c.table, v))
                    break
        if len(prob) == len(variables):
            for t in prob:
                div = t.table[0][0] + t.table[0][1]
                for j in range(2):
                    t.table[0][j] /= div
            return prob
        print("Error")


def getJT(name):
    ts = beliefTable.modelBTs(name)
    j = JunctionTree(name)
    if name == 'asia':
        j.addCluster(variables=['tub', 'asia'], table=beliefTable.multiplyBTs(ts[0], ts[1]))
        j.addCluster(variables=['tub'], table=beliefTable.BeliefTable(variables=['tub'], table=[[1, 1]]),
                     neighbours=[['tub', 'asia']],
                     separator=True)
        j.addCluster(variables=['either', 'lung', 'tub'], table=ts[5], neighbours=[['tub']])
        j.addCluster(variables=['either'], table=beliefTable.BeliefTable(variables=['either'], table=[[1, 1]]),
                     neighbours=[['either', 'lung', 'tub']],
                     separator=True)
        j.addCluster(variables=['xray', 'either'], table=ts[6], neighbours=[['either']])
        j.addCluster(variables=['either', 'lung'],
                     table=beliefTable.BeliefTable(variables=['either', 'lung'], table=[[1, 1], [1, 1]]),
                     neighbours=[['either', 'lung', 'tub']],
                     separator=True)
        j.addCluster(variables=['either', 'smoke', 'lung'], table=beliefTable.multiplyBTs(ts[2], ts[3]),
                     neighbours=[['either', 'lung']])
        j.addCluster(variables=['either', 'smoke'],
                     table=beliefTable.BeliefTable(variables=['either', 'smoke'], table=[[1, 1], [1, 1]]),
                     neighbours=[['either', 'smoke', 'lung']],
                     separator=True)
        j.addCluster(variables=['either', 'smoke', 'bronc'], table=ts[4],
                     neighbours=[['either', 'smoke']])
        j.addCluster(variables=['either', 'bronc'],
                     table=beliefTable.BeliefTable(variables=['either', 'bronc'], table=[[1, 1], [1, 1]]),
                     neighbours=[['either', 'smoke', 'bronc']],
                     separator=True)
        j.addCluster(variables=['dysp', 'bronc', 'either'], table=ts[7],
                     neighbours=[['either', 'bronc']])
    elif name == 'cancer':
        j.addCluster(variables=['cancer', 'dyspnea'], table=ts[4])
        j.addCluster(variables=['cancer1'], table=beliefTable.BeliefTable(variables=['cancer'], table=[[1, 1]]),
                     neighbours=[['cancer', 'dyspnea']],
                     separator=True)
        j.addCluster(variables=['cancer', 'smoker', 'pollution'],
                     table=beliefTable.multiplyBTs(beliefTable.multiplyBTs(ts[0], ts[1]), ts[2]),
                     neighbours=[['cancer1']])
        j.addCluster(variables=['cancer2'], table=beliefTable.BeliefTable(variables=['cancer'], table=[[1, 1]]),
                     neighbours=[['cancer', 'dyspnea']],
                     separator=True)
        j.addCluster(variables=['xray', 'cancer'], table=ts[3], neighbours=[['cancer2']])
    elif name == 'sprinkler':
        j.addCluster(variables=['rain', 'sprinkler', 'cloudy'],
                     table=beliefTable.multiplyBTs(beliefTable.multiplyBTs(ts[0], ts[1]), ts[2]))
        j.addCluster(variables=['rain', 'sprinkler'],
                     table=beliefTable.BeliefTable(variables=['rain', 'sprinkler'], table=[[1, 1], [1, 1]]),
                     neighbours=[['rain', 'sprinkler', 'cloudy']],
                     separator=True)
        j.addCluster(variables=['rain', 'sprinkler', 'wet_grass'],
                     table=ts[3],
                     neighbours=[['rain', 'sprinkler']])
    return j


print('ASIA:')
model = getJT('asia')

variables = ['asia', 'smoke', 'dysp']
evidences = [False, True, True]
model.setEvidence(variables, evidences)

prob = model.getProb(['asia', 'bronc', 'dysp', 'either', 'lung', 'smoke', 'tub', 'xray'])
print('evidences: ' + str(model.evidences))
for p in prob:
    p.print()

print()
print('CANCER:')

model = getJT('cancer')

variables = ['pollution', 'smoker']
evidences = [False, True]
model.setEvidence(variables, evidences)

prob = model.getProb(['cancer', 'dyspnea', 'pollution', 'smoker', 'xray'])
print('evidences: ' + str(model.evidences))
for p in prob:
    p.print()

print()
print('SPRINKLER:')

model = getJT('sprinkler')

variables = ['cloudy', 'wet_grass']
evidences = [True, True]
model.setEvidence(variables, evidences)

prob = model.getProb(['cloudy', 'rain', 'sprinkler', 'wet_grass'])
print('evidences: ' + str(model.evidences))
for p in prob:
    p.print()
