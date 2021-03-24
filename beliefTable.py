class BeliefTable(object):

    def __init__(self, variables, table, joint=False):
        # variables = a list of strings (names of variables)
        # table = a list of list of float (representing a table)
        # conditioned = a boolean (for separate joint prob from conditioned prob)
        self.variables = variables
        self.table = table
        self.joint = joint

    def putEvidence(self, variable, value):
        # variable: variable name (string)
        # value: boolean
        if variable in self.variables:
            index = self.variables.index(variable)
            if index == 0:
                if value:
                    for i in self.table:
                        i[1] = 0
                else:
                    for i in self.table:
                        i[0] = 0
            elif index == 1:
                if len(self.variables) == 2:
                    if value:
                        for k in range(2):
                            self.table[1][k] = 0
                    else:
                        for k in range(2):
                            self.table[0][k] = 0
                if len(self.variables) == 3:
                    if value:
                        for i in range(2, 4):
                            for k in range(2):
                                self.table[i][k] = 0
                    else:
                        for i in range(0, 2):
                            for k in range(2):
                                self.table[i][k] = 0
            elif index == 2:
                if value:
                    for i in range(1, 4, 2):
                        for k in range(2):
                            self.table[i][k] = 0
                else:
                    for i in range(0, 4, 2):
                        for k in range(2):
                            self.table[i][k] = 0

    def print(self):
        table = self.table
        for i in range(len(table)):
            for j in range(2):
                table[i][j] = round(table[i][j] * 100, 2)
        s = ''
        for i in self.variables:
            s = s + i + ', '
        s = s[:len(s) - 2]
        print(s + ': ' + str(table))


def marginalize(table, variable):
    # table = a belief joint table
    # variable = a string (name of a variable)
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
    elif len(table.variables) == 3:
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
    return BeliefTable(variables=[variable], table=[t], joint=True)


def marginalizeMSG(table, variables):
    # table: BT
    # variables: array of variables (strings)
    if len(variables) == 1:
        return marginalize(table, variables[0])
    else:
        t = []
        if variables[0] == table.variables[0] and variables[1] == table.variables[1]:
            t.append([table.table[0][0] + table.table[1][0], table.table[0][1] + table.table[1][1]])
            t.append([table.table[2][0] + table.table[3][0], table.table[2][1] + table.table[3][1]])
        elif variables[0] == table.variables[0] and variables[1] == table.variables[2]:
            t.append([table.table[0][0] + table.table[2][0], table.table[0][1] + table.table[2][1]])
            t.append([table.table[1][0] + table.table[3][0], table.table[1][1] + table.table[3][1]])
        elif variables[0] == table.variables[1] and variables[1] == table.variables[0]:
            variables[0], variables[1] = variables[1], variables[0]
            return marginalizeMSG(table, variables)
        elif variables[0] == table.variables[1] and variables[1] == table.variables[2]:
            t.append([table.table[0][0] + table.table[0][1], table.table[2][0] + table.table[2][1]])
            t.append([table.table[1][0] + table.table[1][1], table.table[3][0] + table.table[3][1]])
            return BeliefTable(variables=variables, table=t, joint=True)
        elif variables[0] == table.variables[2] and variables[1] == table.variables[0]:
            variables[0], variables[1] = variables[1], variables[0]
            return marginalizeMSG(table, variables)
        elif variables[0] == table.variables[2] and variables[1] == table.variables[1]:
            variables[0], variables[1] = variables[1], variables[0]
            return marginalizeMSG(table, variables)
    return BeliefTable(variables=variables, table=t, joint=True)


def multiplyBTs(table1, table2):
    t = []
    if len(table1.variables) == 1 and len(table2.variables) == 1:
        if table1.variables[0] == table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][1]])
            return BeliefTable(variables=[table2.variables[0]], table=t, joint=True)
        else:
            for i in table2.table[0]:
                tmp = []
                for j in table1.table[0]:
                    tmp.append(i * j)
                t.append(tmp)
            return BeliefTable(variables=[table1.variables[0], table2.variables[0]], table=t, joint=True)
    elif len(table1.variables) == 1 and len(table2.variables) == 2:
        if table1.variables[0] == table2.variables[1]:
            j = iter(table2.table)
            for i in table1.table[0]:
                tmp = []
                for k in next(j):
                    tmp.append(k * i)
                t.append(tmp)
            return BeliefTable(variables=[table2.variables[0], table1.variables[0]], table=t, joint=True)
        elif table1.variables[0] == table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][0] * table2.table[0][1]])
            t.append([table1.table[0][1] * table2.table[1][0], table1.table[0][1] * table2.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        else:
            # tabella a 3
            return None
    elif len(table1.variables) == 2 and len(table2.variables) == 1:
        return multiplyBTs(table2, table1)
    elif len(table1.variables) == 2 and len(table2.variables) == 2:
        if table1.variables[0] == table2.variables[0] and table1.variables[1] == table2.variables[1]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][1]])
            t.append([table1.table[1][0] * table2.table[1][0], table1.table[1][1] * table2.table[1][1]])
        elif table1.variables[0] == table2.variables[1] and table1.variables[1] == table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[1][0]])
            t.append([table1.table[1][0] * table2.table[0][1], table1.table[1][1] * table2.table[1][1]])
        elif table1.variables[0] == table2.variables[0] and table1.variables[1] != table2.variables[1]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][1]])
            t.append([table1.table[0][0] * table2.table[1][0], table1.table[0][1] * table2.table[1][1]])
            t.append([table1.table[1][0] * table2.table[0][0], table1.table[1][1] * table2.table[0][1]])
            t.append([table1.table[1][0] * table2.table[1][0], table1.table[1][1] * table2.table[1][1]])
            vs = []
            for v in table1.variables:
                vs.append(v)
            vs.append(table2.variables[1])
            return BeliefTable(variables=vs, table=t)
        elif table1.variables[1] == table2.variables[1] and table1.variables[0] != table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][0]])
            t.append([table1.table[0][0] * table2.table[0][1], table1.table[0][1] * table2.table[0][1]])
            t.append([table1.table[1][0] * table2.table[1][0], table1.table[1][1] * table2.table[1][0]])
            t.append([table1.table[1][0] * table2.table[1][1], table1.table[1][1] * table2.table[1][1]])
            vs = table1.variables
            vs.append(table2.variables[0])
            return BeliefTable(variables=vs, table=t)
        elif table1.variables[1] == table2.variables[0] and table1.variables[0] != table2.variables[1]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][0]])
            t.append([table1.table[1][0] * table2.table[0][1], table1.table[1][1] * table2.table[0][1]])
            t.append([table1.table[0][0] * table2.table[1][0], table1.table[0][1] * table2.table[1][0]])
            t.append([table1.table[1][0] * table2.table[1][1], table1.table[1][1] * table2.table[1][1]])
            vs = []
            vs.append(table1.variables[0])
            vs.append(table2.variables[1])
            vs.append(table2.variables[0])
            return BeliefTable(variables=vs, table=t)
        return BeliefTable(variables=table1.variables, table=t)
    elif len(table1.variables) == 1 and len(table2.variables) == 3:
        if table1.variables[0] == table2.variables[0]:
            for j in table2.table:
                i = iter(table1.table[0])
                t.append([j[0] * next(i), j[1] * next(i)])
        elif table1.variables[0] == table2.variables[1]:
            i = iter(table1.table[0])
            val = next(i)
            first = True
            second = False
            change = False
            for j in table2.table:
                if second:
                    change = True
                if first:
                    first = False
                    second = True
                if change:
                    val = next(i)
                t.append([j[0] * val, j[1] * val])

        elif table1.variables[0] == table2.variables[2]:
            yes = True
            for j in table2.table:
                if yes:
                    yes = False
                    t.append([j[0] * table1.table[0][0], j[1] * table1.table[0][0]])
                else:
                    yes = True
                    t.append([j[0] * table1.table[0][1], j[1] * table1.table[0][1]])
        else:
            return None
        return BeliefTable(variables=table2.variables, table=t)
    elif len(table1.variables) == 3 and len(table2.variables) == 1:
        return multiplyBTs(table2, table1)
    elif len(table1.variables) == 2 and len(table2.variables) == 3:
        if table1.variables[0] == table2.variables[1] and table1.variables[1] == table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][0]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][1] * table1.table[1][0]])
            t.append([table2.table[2][0] * table1.table[0][1], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[1][1], table2.table[3][1] * table1.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        elif table1.variables[0] == table2.variables[2] and table1.variables[1] == table2.variables[1]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][0]])
            t.append([table2.table[1][0] * table1.table[0][1], table2.table[1][1] * table1.table[0][1]])
            t.append([table2.table[2][0] * table1.table[1][0], table2.table[2][1] * table1.table[1][0]])
            t.append([table2.table[3][0] * table1.table[1][1], table2.table[3][1] * table1.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        elif table1.variables[0] == table2.variables[0] and table1.variables[1] == table2.variables[1]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[0][0], table2.table[1][1] * table1.table[0][1]])
            t.append([table2.table[2][0] * table1.table[1][0], table2.table[2][1] * table1.table[1][1]])
            t.append([table2.table[3][0] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        elif table1.variables[0] == table2.variables[0] and table1.variables[1] == table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        elif table1.variables[0] == table2.variables[2] and table1.variables[1] == table2.variables[0]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[1][0]])
            t.append([table2.table[1][0] * table1.table[0][1], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][1] * table1.table[1][0]])
            t.append([table2.table[3][0] * table1.table[0][1], table2.table[3][1] * table1.table[1][1]])
            return BeliefTable(variables=table2.variables, table=t)
        else:
            return None
    elif len(table1.variables) == 3 and len(table2.variables) == 2:
        return multiplyBTs(table2, table1)


def divideBTs(table1, table2):  # return table1/table2
    if set(table1.variables).issubset(set(table2.variables)) and set(table2.variables).issubset(set(table1.variables)):
        t = []
        j = iter(table2.table)
        spec = True
        for count in range(len(table1.variables)):
            if table1.variables[count] != table2.variables[count]:
                spec = False
        if spec:
            for i in table1.table:
                val = next(j)
                tmp = []
                for k in range(len(i)):
                    if val[k] == 0:
                        tmp.append(0)
                    else:
                        tmp.append(i[k] / val[k])
                t.append(tmp)
        else:
            k = 0
            for i in table1.table:
                val = next(j)
                tmp = []
                if val[k] == 0:
                    tmp.append(0)
                else:
                    tmp.append(i[0] / val[k])
                val = next(j)
                if val[k] == 0:
                    tmp.append(0)
                else:
                    tmp.append(i[1] / val[k])
                t.append(tmp)
                k += 1
                j = iter(table2.table)
        return BeliefTable(variables=table1.variables, table=t)
    else:
        return None


def modelBTs(name):
    ts = []
    if name == 'asia':
        ts.append(BeliefTable(['asia'], [[0.01, 0.99]]))
        ts.append(BeliefTable(['tub', 'asia'], [[0.05, 0.95], [0.01, 0.99]]))
        ts.append(BeliefTable(['smoke'], [[0.5, 0.5]]))
        ts.append(BeliefTable(['lung', 'smoke'], [[0.1, 0.9], [0.01, 0.99]]))
        ts.append(BeliefTable(['bronc', 'smoke'], [[0.6, 0.4], [0.3, 0.7]]))
        ts.append(BeliefTable(['either', 'lung', 'tub'], [[1, 0], [1, 0], [1, 0], [0, 1]]))
        ts.append(BeliefTable(['xray', 'either'], [[0.98, 0.02], [0.05, 0.95]]))
        ts.append(BeliefTable(['dysp', 'bronc', 'either'], [[0.9, 0.1], [0.7, 0.3], [0.8, 0.2], [0.1, 0.9]]))
    elif name == 'cancer':
        ts.append(BeliefTable(['pollution'], [[0.9, 0.1]]))
        ts.append(BeliefTable(['smoker'], [[0.3, 0.7]]))
        ts.append(BeliefTable(['cancer', 'smoker', 'pollution'],
                              [[0.05, 0.95], [0.03, 0.97], [0.02, 0.98], [0.001, 0.999]]))
        ts.append(BeliefTable(['xray', 'cancer'], [[0.9, 0.1], [0.2, 0.8]]))
        ts.append(BeliefTable(['dyspnea', 'cancer'], [[0.65, 0.35], [0.3, 0.7]]))
    elif name == 'sprinkler':
        ts.append(BeliefTable(['cloudy'], [[0.5, 0.5]]))
        ts.append(BeliefTable(['sprinkler', 'cloudy'], [[0.5, 0.5], [0.9, 0.1]]))
        ts.append(BeliefTable(['rain', 'cloudy'], [[0.8, 0.2], [0.2, 0.8]]))
        ts.append(BeliefTable(['wet_grass', 'sprinkler', 'rain'],
                              [[1, 0], [0.9, 0.1], [0.9, 0.1], [0.01, 0.99]]))
    return ts
