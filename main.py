import bnlearn
import numpy as np

'''
Given a Bayesian Network, put the evidence and, through message passing, get the probability
of a random variable conditioned by evidence p(V|e).
'''


def getJunctionBTs(model):
    tables = dict()
    cpds = model['model'].cpds
    for i in range(len(cpds)):
        tables[getKey(cpds[i].variables)] = getList(cpds[i].values)
    return tables


def getList(ndArray):
    tmp = list()
    for i in range(len(ndArray)):
        tmp.append(ndArray[i])
    return tmp


def getKey(variables):
    n = str(variables[0]) + ' |'
    c = False
    for i in range(1, len(variables)):
        c = True
        n = n + ' ' + str(variables[i]) + ','
    if c:
        n = n[:len(n) - 1]
    else:
        n = n[:len(n) - 2]
    return n


def printTables(table):
    for i in table.keys():
        print(i + ':')
        print(table[i])
        print()


def mulBF(tables):
    t = list()
    if len(tables) == 2:
        t1 = tables[0]
        t2 = tables[1]
        for i in range(len(t1)):
            tmp = list()
            for j in range(len(t2)):
                tmp.append(t2[j][i] * t1[i])
            t.append(tmp)
    elif len(tables) == 3:
        t1 = tables[0]
        t2 = tables[1]
        t3 = tables[3]
        for i in range(len(t1)):
            for j in range(t2):
                tmp = list()
                for k in range(len(t3)):
                    tmp.append(t3[k][i] * t2[j] * t1[i])
                t.append(tmp)
    return t


def marginalize(table, first=True):
    t = list()
    if first:
        for i in range(2):
            sum = 0
            for j in range(len(table)):
                sum += table[j][i]
            t.append(sum)
    else:
        for j in range(len(table)):
            sum = 0
            for i in range(2):
                sum += table[j][i]
            t.append(sum)
    return t


def getClustersBTs(model):
    tables = dict()
    if model == 'asia':
        tables['asia, tub'] = [(0.0005, 0.0095), (0.0099, 0.981)]
        a = tables['asia, tub'][0]
        b = tables['asia, tub'][0][0]
        tables['either, xray'] = [0.0005, 0.0095]
        tables['tub, either, lung'] = [0.0005, 0.0095]
        tables['either, lung, smoke'] = [0.0005, 0.0095]
        tables['either, smoke, bronc'] = [0.0005, 0.0095]
        tables['either, bronc, dysp'] = [0.0005, 0.0095]

        tables['tub'] = [0.0005, 0.0095]
        tables['either'] = [0.0005, 0.0095]
        tables['either, lung'] = [0.0005, 0.0095]
        tables['either, smoke'] = [0.0005, 0.0095]
        tables['either, bronc'] = [0.0005, 0.0095]

## Asia model, p(L|A=1,S=0,D=1)
asia = dict(bnlearn.import_DAG('asia'))
## G1 = bnlearn.plot(model)
#junctionBTs = dict(getJunctionBTs(asia))  # asia['model'].cpds.values
# table = mulBF([junctionBTs['asia'], junctionBTs['tub | asia']])
# table2 = mulBF([])
# clusterBTs = getClustersBTs('asia')
q1 = bnlearn.inference.fit(asia, variables=['bronc'], evidence={'asia':1,'smoke':0, 'dysp':0})

## Sprinkler model, p(S|W=1)
# sprinkler = dict(bnlearn.import_DAG('sprinkler'))
##G2 = bnlearn.plot(sprinkler)
# q2 = bnlearn.inference.fit(sprinkler, variables=['Sprinkler'], evidence={'Wet_Grass': 1})

## Cancer model, p(C|S=0,P=1)
# cancer = dict(bnlearn.import_DAG('cancer.bif'))
## G3 = bnlearn.plot(model3)
# q3 = bnlearn.inference.fit(cancer, variables=['Cancer'], evidence={'Smoker': 0, 'Pollution': 1})
