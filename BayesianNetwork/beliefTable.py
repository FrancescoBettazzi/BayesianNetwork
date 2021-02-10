class BeliefTable(object):

    def __init__(self, variables, table):
        self.variables = variables
        self.table = table

    def print(self):
        s = ''
        for i in self.variables:
            s = s + i + ', '
        s = s[:len(s) - 2]
        print(s + ': ' + str(self.table))


def getJoint2(table1, table2):
    # table1 = prob di prima variabile
    # table2 = prob condizionata
    t = []
    k = 0
    for i in table1.table:
        t.append([table2.table[k][0] * i, table2.table[k][1] * i])
        k += 1
    return BeliefTable(variables=[table2.variables[0], table1.variables[0]], table=t)


def getJoint3(table1, table2, table3):
    # table1 = prob di prima variabile
    # table2 = prob di seconda variabile
    # table3 = prob condizionata
    t = []
    k = 0
    for i in table1.table:
        for j in table2.table:
            t.append([table3.table[k][0] * i * j, table3.table[k][1] * i * j])
            k += 1
    return BeliefTable(variables=[table3.variables[0], table1.variables[0], table2.variables[0]], table=t)


def marginalize(table, variable):
    # table = joint table
    # variable = nome di una variabile
    index = table.variables.index(variable)
    t = []
    sum1 = 0
    sum2 = 0
    if len(table.variables) == 2:
        if index == 0:
            for i in table.table:
                sum1 += i[0]
                sum2 += i[1]
            t.append(sum1)
            t.append(sum2)
        elif index == 1:
            for i in table.table:
                t.append(i[0] + i[1])
    if len(table.variables) == 3:
        if index == 0:
            for i in table.table:
                sum1 += i[0]
                sum2 += i[1]
            t.append(sum1)
            t.append(sum2)
        elif index == 1:
            for i in range(len(table.table)):
                if i < 2:
                    sum1 += table.table[i][0] + table.table[i][1]
                else:
                    sum2 += table.table[i][0] + table.table[i][1]
            t.append(sum1)
            t.append(sum2)
        elif index == 2:
            for i in range(len(table.table)):
                if i % 2 == 0:
                    sum1 += table.table[i][0] + table.table[i][1]
                else:
                    sum2 += table.table[i][0] + table.table[i][1]
            t.append(sum1)
            t.append(sum2)
    return BeliefTable(variables=[variable], table=t)


table1 = BeliefTable(['asia'], [0.01, 0.99])
table2 = BeliefTable(['tub', 'asia'], [[0.05, 0.95], [0.01, 0.99]])
t = getJoint2(table1, table2)
print(t.table)
t1 = BeliefTable(['either', 'lung', 'tub'], [[1, 0], [1, 0], [1, 0], [0, 1]])
t2 = BeliefTable(['lung'], [0.055, 0.945])
t3 = BeliefTable(['tub'], [0.0104, 0.9896])
tr = getJoint3(t2, t3, t1)
print(tr.table)
dbe = BeliefTable(['dysp', 'bronc', 'either'], [[0.9, 0.1], [0.7, 0.3], [0.8, 0.2], [0.1, 0.9]])
b = BeliefTable(['bronc'], [0.45, 0.55])
e = BeliefTable(['either'], [0.064828, 0.935172])
joint = getJoint3(b, e, dbe)
print(joint.table)

asia = marginalize(t, 'asia')
tub_asia = marginalize(t, 'tub')
either_either = marginalize(tr, 'either')
lung = marginalize(tr, 'lung')
# tub_either = marginalize(tr, 'tub')
dysp = marginalize(joint, 'dysp')
bronc = marginalize(joint, 'bronc')
# either_dysp = marginalize(joint, 'either')

asia.print()
tub_asia.print()
either_either.print()
lung.print()
# tub_either.print()
dysp.print()
bronc.print()
# either_dysp.print()
