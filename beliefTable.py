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
                    pos = 1
                else:
                    pos = 0
                for i in self.table:
                    i[pos] = 0
            else:
                count = len(self.variables) - index
                for i in range(len(self.table)):
                    if count > 0:
                        if not value:
                            self.table[i][0] = 0
                            self.table[i][1] = 0
                        count -= 1
                    else:
                        if value:
                            self.table[i][0] = 0
                            self.table[i][1] = 0
                        count -= 1
                        if count == -(len(self.variables) - index):
                            count = len(self.variables) - index

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
    # table = a belief table
    # variable = a string (name of a variable)
    index = table.variables.index(variable)
    t = []
    sum1 = 0
    sum2 = 0
    if index == 0:
        for i in table.table:
            sum1 += i[0]
            sum2 += i[1]
        t.append(sum1)
        t.append(sum2)
    else:
        count = len(table.variables) - index
        for i in range(len(table.table)):
            if count > 0:
                sum1 += table.table[i][0] + table.table[i][1]
                count -= 1
            else:
                sum2 += table.table[i][0] + table.table[i][1]
                count -= 1
                if count == -(len(table.variables) - index):
                    count = len(table.variables) - index
        t.append(sum1)
        t.append(sum2)
    return BeliefTable(variables=[variable], table=[t], joint=True)


def marginalizeMSG(table, variables):
    # table: BT
    # variables: array of variables (strings)
    t = []
    if len(variables) == 1:
        return marginalize(table, variables[0])
    elif len(variables) == 2:
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
            return BeliefTable(variables=variables, table=t)
        elif variables[0] == table.variables[2] and variables[1] == table.variables[0]:
            variables[0], variables[1] = variables[1], variables[0]
            return marginalizeMSG(table, variables)
        elif variables[0] == table.variables[2] and variables[1] == table.variables[1]:
            variables[0], variables[1] = variables[1], variables[0]
            return marginalizeMSG(table, variables)
    return BeliefTable(variables=variables, table=t)


def multiplyBTs(table1, table2):
    t = []
    vs = None
    if len(table1.variables) == 1 and len(table2.variables) == 1:
        if table1.variables[0] == table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][1]])
            vs = [table2.variables[0]]
        else:
            for i in table2.table[0]:
                tmp = []
                for j in table1.table[0]:
                    tmp.append(i * j)
                t.append(tmp)
            vs = [table1.variables[0], table2.variables[0]]

    elif len(table1.variables) == 1 and len(table2.variables) == 2:
        if table1.variables[0] == table2.variables[1]:
            j = iter(table2.table)
            for i in table1.table[0]:
                tmp = []
                for k in next(j):
                    tmp.append(k * i)
                t.append(tmp)
            vs = [table2.variables[0], table1.variables[0]]
        elif table1.variables[0] == table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][0] * table2.table[0][1]])
            t.append([table1.table[0][1] * table2.table[1][0], table1.table[0][1] * table2.table[1][1]])
            vs = []
            for v in table2.variables:
                vs.append(v)
        else:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][0]])
            t.append([table1.table[0][0] * table2.table[0][1], table1.table[0][1] * table2.table[0][1]])
            t.append([table1.table[0][0] * table2.table[1][0], table1.table[0][1] * table2.table[1][0]])
            t.append([table1.table[0][0] * table2.table[1][1], table1.table[0][1] * table2.table[1][1]])
            vs = []
            vs.append(table1.variables[0])
            vs.append(table2.variables[1])
            vs.append(table2.variables[0])

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
        elif table1.variables[1] == table2.variables[1] and table1.variables[0] != table2.variables[0]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][0]])
            t.append([table1.table[0][0] * table2.table[0][1], table1.table[0][1] * table2.table[0][1]])
            t.append([table1.table[1][0] * table2.table[1][0], table1.table[1][1] * table2.table[1][0]])
            t.append([table1.table[1][0] * table2.table[1][1], table1.table[1][1] * table2.table[1][1]])
            vs = []
            for v in table1.variables:
                vs.append(v)
            vs.append(table2.variables[0])
        elif table1.variables[1] == table2.variables[0] and table1.variables[0] != table2.variables[1]:
            t.append([table1.table[0][0] * table2.table[0][0], table1.table[0][1] * table2.table[0][0]])
            t.append([table1.table[1][0] * table2.table[0][1], table1.table[1][1] * table2.table[0][1]])
            t.append([table1.table[0][0] * table2.table[1][0], table1.table[0][1] * table2.table[1][0]])
            t.append([table1.table[1][0] * table2.table[1][1], table1.table[1][1] * table2.table[1][1]])
            vs = []
            vs.append(table1.variables[0])
            vs.append(table2.variables[1])
            vs.append(table2.variables[0])
        if vs == None:
            vs = []
            for v in table1.variables:
                vs.append(v)

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
        vs = []
        for v in table2.variables:
            vs.append(v)

    elif len(table1.variables) == 2 and len(table2.variables) == 3:
        vs = []
        if table1.variables[0] == table2.variables[1] and table1.variables[1] == table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][0]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][1] * table1.table[1][0]])
            t.append([table2.table[2][0] * table1.table[0][1], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[1][1], table2.table[3][1] * table1.table[1][1]])
        elif table1.variables[0] == table2.variables[2] and table1.variables[1] == table2.variables[1]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][0]])
            t.append([table2.table[1][0] * table1.table[0][1], table2.table[1][1] * table1.table[0][1]])
            t.append([table2.table[2][0] * table1.table[1][0], table2.table[2][1] * table1.table[1][0]])
            t.append([table2.table[3][0] * table1.table[1][1], table2.table[3][1] * table1.table[1][1]])
        elif table1.variables[0] == table2.variables[0] and table1.variables[1] == table2.variables[1]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[0][0], table2.table[1][1] * table1.table[0][1]])
            t.append([table2.table[2][0] * table1.table[1][0], table2.table[2][1] * table1.table[1][1]])
            t.append([table2.table[3][0] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])
        elif table1.variables[0] == table2.variables[0] and table1.variables[1] == table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])
        elif table1.variables[0] == table2.variables[2] and table1.variables[1] == table2.variables[0]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[1][0]])
            t.append([table2.table[1][0] * table1.table[0][1], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][1] * table1.table[1][0]])
            t.append([table2.table[3][0] * table1.table[0][1], table2.table[3][1] * table1.table[1][1]])
        elif table1.variables[1] == table2.variables[0] and table1.variables[0] != table2.variables[1] and \
                table1.variables[0] != table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[0][1]])
            t.append([table2.table[0][1] * table1.table[1][0], table2.table[0][1] * table1.table[1][1]])
            t.append([table2.table[1][0] * table1.table[0][0], table2.table[1][0] * table1.table[0][1]])
            t.append([table2.table[1][1] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][0] * table1.table[0][1]])
            t.append([table2.table[2][1] * table1.table[1][0], table2.table[2][1] * table1.table[1][1]])
            t.append([table2.table[3][0] * table1.table[0][0], table2.table[3][0] * table1.table[0][1]])
            t.append([table2.table[3][1] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])

            vs.append(table1.variables[0])
            vs.append(table2.variables[1])
            vs.append(table2.variables[2])
            vs.append(table2.variables[0])

        if len(vs) == 0:
            for v in table2.variables:
                vs.append(v)

    elif len(table1.variables) == 3 and len(table2.variables) == 3:
        vs = []
        if table1.variables[0] == table2.variables[1] and table1.variables[1] != table2.variables[0] and \
                table1.variables[2] == table2.variables[2]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[2][0]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][0] * table1.table[3][0]])
            t.append([table2.table[2][0] * table1.table[0][1], table2.table[2][0] * table1.table[2][1]])
            t.append([table2.table[3][0] * table1.table[1][1], table2.table[3][0] * table1.table[3][1]])
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][1] * table1.table[2][0]])
            t.append([table2.table[1][1] * table1.table[1][0], table2.table[1][1] * table1.table[3][0]])
            t.append([table2.table[2][1] * table1.table[0][1], table2.table[2][1] * table1.table[2][1]])
            t.append([table2.table[3][1] * table1.table[1][1], table2.table[3][1] * table1.table[3][1]])

            vs.append(table1.variables[1])
            for v in table2.variables:
                vs.append(v)
    elif len(table1.variables) == 2 and len(table2.variables) == 4:
        vs = []
        if table1.variables[1] == table2.variables[3] and (
                table1.variables[0] not in [x for x in table2.variables if x != table2.variables[3]]):
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[0][1]])
            t.append([table2.table[0][1] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][0] * table1.table[1][1]])
            t.append([table2.table[1][1] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][0] * table1.table[0][1]])
            t.append([table2.table[2][1] * table1.table[0][0], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[1][0], table2.table[3][0] * table1.table[1][1]])
            t.append([table2.table[3][1] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])
            t.append([table2.table[4][0] * table1.table[0][0], table2.table[4][0] * table1.table[0][1]])
            t.append([table2.table[4][1] * table1.table[0][0], table2.table[4][1] * table1.table[0][1]])
            t.append([table2.table[5][0] * table1.table[1][0], table2.table[5][0] * table1.table[1][1]])
            t.append([table2.table[5][1] * table1.table[1][0], table2.table[5][1] * table1.table[1][1]])
            t.append([table2.table[6][0] * table1.table[0][0], table2.table[6][0] * table1.table[0][1]])
            t.append([table2.table[6][1] * table1.table[0][0], table2.table[6][1] * table1.table[0][1]])
            t.append([table2.table[7][0] * table1.table[1][0], table2.table[7][0] * table1.table[1][1]])
            t.append([table2.table[7][1] * table1.table[1][0], table2.table[7][1] * table1.table[1][1]])
            vs = []
            vs.append(table1.variables[0])
            for i in range(1, len(table2.variables)):
                vs.append(table2.variables[i])
            vs.append(table2.variables[0])
    elif len(table1.variables) == 3 and len(table2.variables) == 5:
        vs = []
        if table1.variables[1] == table2.variables[4] and table1.variables[2] == table2.variables[2] and (
                table1.variables[0] not in [x for x in table2.variables if
                                            x not in [table2.variables[2], table2.variables[4]]]):
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[0][1]])
            t.append([table2.table[0][1] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[2][0], table2.table[1][0] * table1.table[2][1]])
            t.append([table2.table[1][1] * table1.table[2][0], table2.table[1][1] * table1.table[2][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][0] * table1.table[0][1]])
            t.append([table2.table[2][1] * table1.table[0][0], table2.table[2][1] * table1.table[0][1]])
            t.append([table2.table[3][0] * table1.table[2][0], table2.table[3][0] * table1.table[2][1]])
            t.append([table2.table[3][1] * table1.table[2][0], table2.table[3][1] * table1.table[2][1]])

            t.append([table2.table[4][0] * table1.table[1][0], table2.table[4][0] * table1.table[1][1]])
            t.append([table2.table[4][1] * table1.table[1][0], table2.table[4][1] * table1.table[1][1]])
            t.append([table2.table[5][0] * table1.table[3][0], table2.table[5][0] * table1.table[3][1]])
            t.append([table2.table[5][1] * table1.table[3][0], table2.table[5][1] * table1.table[3][1]])
            t.append([table2.table[6][0] * table1.table[1][0], table2.table[6][0] * table1.table[1][1]])
            t.append([table2.table[6][1] * table1.table[1][0], table2.table[6][1] * table1.table[1][1]])
            t.append([table2.table[7][0] * table1.table[3][0], table2.table[7][0] * table1.table[3][1]])
            t.append([table2.table[7][1] * table1.table[3][0], table2.table[7][1] * table1.table[3][1]])

            t.append([table2.table[8][0] * table1.table[0][0], table2.table[8][0] * table1.table[0][1]])
            t.append([table2.table[8][1] * table1.table[0][0], table2.table[8][1] * table1.table[0][1]])
            t.append([table2.table[9][0] * table1.table[2][0], table2.table[9][0] * table1.table[2][1]])
            t.append([table2.table[9][1] * table1.table[2][0], table2.table[9][1] * table1.table[2][1]])
            t.append([table2.table[10][0] * table1.table[0][0], table2.table[10][0] * table1.table[0][1]])
            t.append([table2.table[10][1] * table1.table[0][0], table2.table[10][1] * table1.table[0][1]])
            t.append([table2.table[11][0] * table1.table[2][0], table2.table[11][0] * table1.table[2][1]])
            t.append([table2.table[11][1] * table1.table[2][0], table2.table[11][1] * table1.table[2][1]])

            t.append([table2.table[12][0] * table1.table[1][0], table2.table[12][0] * table1.table[1][1]])
            t.append([table2.table[12][1] * table1.table[1][0], table2.table[12][1] * table1.table[1][1]])
            t.append([table2.table[13][0] * table1.table[3][0], table2.table[13][0] * table1.table[3][1]])
            t.append([table2.table[13][1] * table1.table[3][0], table2.table[13][1] * table1.table[3][1]])
            t.append([table2.table[14][0] * table1.table[1][0], table2.table[14][0] * table1.table[1][1]])
            t.append([table2.table[14][1] * table1.table[1][0], table2.table[14][1] * table1.table[1][1]])
            t.append([table2.table[15][0] * table1.table[3][0], table2.table[15][0] * table1.table[3][1]])
            t.append([table2.table[15][1] * table1.table[3][0], table2.table[15][1] * table1.table[3][1]])

            vs = []
            vs.append(table1.variables[0])
            for i in range(1, len(table2.variables)):
                vs.append(table2.variables[i])
            vs.append(table2.variables[0])
    elif len(table1.variables) == 2 and len(table2.variables) == 6:
        if table1.variables[1] == table2.variables[0] and table1.variables[0] not in [x for x in table2.variables if
                                                                                      x != table2.variables[0]]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[0][1]])
            t.append([table2.table[0][1] * table1.table[1][0], table2.table[0][1] * table1.table[1][1]])
            t.append([table2.table[1][0] * table1.table[0][0], table2.table[1][0] * table1.table[0][1]])
            t.append([table2.table[1][1] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[0][0], table2.table[2][0] * table1.table[0][1]])
            t.append([table2.table[2][1] * table1.table[1][0], table2.table[2][1] * table1.table[1][1]])
            t.append([table2.table[3][0] * table1.table[0][0], table2.table[3][0] * table1.table[0][1]])
            t.append([table2.table[3][1] * table1.table[1][0], table2.table[3][1] * table1.table[1][1]])

            t.append([table2.table[4][0] * table1.table[0][0], table2.table[4][0] * table1.table[0][1]])
            t.append([table2.table[4][1] * table1.table[1][0], table2.table[4][1] * table1.table[1][1]])
            t.append([table2.table[5][0] * table1.table[0][0], table2.table[5][0] * table1.table[0][1]])
            t.append([table2.table[5][1] * table1.table[1][0], table2.table[5][1] * table1.table[1][1]])
            t.append([table2.table[6][0] * table1.table[0][0], table2.table[6][0] * table1.table[0][1]])
            t.append([table2.table[6][1] * table1.table[1][0], table2.table[6][1] * table1.table[1][1]])
            t.append([table2.table[7][0] * table1.table[0][0], table2.table[7][0] * table1.table[0][1]])
            t.append([table2.table[7][1] * table1.table[1][0], table2.table[7][1] * table1.table[1][1]])

            t.append([table2.table[8][0] * table1.table[0][0], table2.table[8][0] * table1.table[0][1]])
            t.append([table2.table[8][1] * table1.table[1][0], table2.table[8][1] * table1.table[1][1]])
            t.append([table2.table[9][0] * table1.table[0][0], table2.table[9][0] * table1.table[0][1]])
            t.append([table2.table[9][1] * table1.table[1][0], table2.table[9][1] * table1.table[1][1]])
            t.append([table2.table[10][0] * table1.table[0][0], table2.table[10][0] * table1.table[0][1]])
            t.append([table2.table[10][1] * table1.table[1][0], table2.table[10][1] * table1.table[1][1]])
            t.append([table2.table[11][0] * table1.table[0][0], table2.table[11][0] * table1.table[0][1]])
            t.append([table2.table[11][1] * table1.table[1][0], table2.table[11][1] * table1.table[1][1]])

            t.append([table2.table[12][0] * table1.table[0][0], table2.table[12][0] * table1.table[0][1]])
            t.append([table2.table[12][1] * table1.table[1][0], table2.table[12][1] * table1.table[1][1]])
            t.append([table2.table[13][0] * table1.table[0][0], table2.table[13][0] * table1.table[0][1]])
            t.append([table2.table[13][1] * table1.table[1][0], table2.table[13][1] * table1.table[1][1]])
            t.append([table2.table[14][0] * table1.table[0][0], table2.table[14][0] * table1.table[0][1]])
            t.append([table2.table[14][1] * table1.table[1][0], table2.table[14][1] * table1.table[1][1]])
            t.append([table2.table[15][0] * table1.table[0][0], table2.table[15][0] * table1.table[0][1]])
            t.append([table2.table[15][1] * table1.table[1][0], table2.table[15][1] * table1.table[1][1]])

            t.append([table2.table[16][0] * table1.table[0][0], table2.table[16][0] * table1.table[0][1]])
            t.append([table2.table[16][1] * table1.table[1][0], table2.table[16][1] * table1.table[1][1]])
            t.append([table2.table[17][0] * table1.table[0][0], table2.table[17][0] * table1.table[0][1]])
            t.append([table2.table[17][1] * table1.table[1][0], table2.table[17][1] * table1.table[1][1]])
            t.append([table2.table[18][0] * table1.table[0][0], table2.table[18][0] * table1.table[0][1]])
            t.append([table2.table[18][1] * table1.table[1][0], table2.table[18][1] * table1.table[1][1]])
            t.append([table2.table[19][0] * table1.table[0][0], table2.table[19][0] * table1.table[0][1]])
            t.append([table2.table[19][1] * table1.table[1][0], table2.table[19][1] * table1.table[1][1]])

            t.append([table2.table[20][0] * table1.table[0][0], table2.table[20][0] * table1.table[0][1]])
            t.append([table2.table[20][1] * table1.table[1][0], table2.table[20][1] * table1.table[1][1]])
            t.append([table2.table[21][0] * table1.table[0][0], table2.table[21][0] * table1.table[0][1]])
            t.append([table2.table[21][1] * table1.table[1][0], table2.table[21][1] * table1.table[1][1]])
            t.append([table2.table[22][0] * table1.table[0][0], table2.table[22][0] * table1.table[0][1]])
            t.append([table2.table[22][1] * table1.table[1][0], table2.table[22][1] * table1.table[1][1]])
            t.append([table2.table[23][0] * table1.table[0][0], table2.table[23][0] * table1.table[0][1]])
            t.append([table2.table[23][1] * table1.table[1][0], table2.table[23][1] * table1.table[1][1]])

            t.append([table2.table[24][0] * table1.table[0][0], table2.table[24][0] * table1.table[0][1]])
            t.append([table2.table[24][1] * table1.table[1][0], table2.table[24][1] * table1.table[1][1]])
            t.append([table2.table[25][0] * table1.table[0][0], table2.table[25][0] * table1.table[0][1]])
            t.append([table2.table[25][1] * table1.table[1][0], table2.table[25][1] * table1.table[1][1]])
            t.append([table2.table[26][0] * table1.table[0][0], table2.table[26][0] * table1.table[0][1]])
            t.append([table2.table[26][1] * table1.table[1][0], table2.table[26][1] * table1.table[1][1]])
            t.append([table2.table[27][0] * table1.table[0][0], table2.table[27][0] * table1.table[0][1]])
            t.append([table2.table[27][1] * table1.table[1][0], table2.table[27][1] * table1.table[1][1]])

            t.append([table2.table[28][0] * table1.table[0][0], table2.table[28][0] * table1.table[0][1]])
            t.append([table2.table[28][1] * table1.table[1][0], table2.table[28][1] * table1.table[1][1]])
            t.append([table2.table[29][0] * table1.table[0][0], table2.table[29][0] * table1.table[0][1]])
            t.append([table2.table[29][1] * table1.table[1][0], table2.table[29][1] * table1.table[1][1]])
            t.append([table2.table[30][0] * table1.table[0][0], table2.table[30][0] * table1.table[0][1]])
            t.append([table2.table[30][1] * table1.table[1][0], table2.table[30][1] * table1.table[1][1]])
            t.append([table2.table[31][0] * table1.table[0][0], table2.table[31][0] * table1.table[0][1]])
            t.append([table2.table[31][1] * table1.table[1][0], table2.table[31][1] * table1.table[1][1]])

            vs = []
            vs.append(table1.variables[0])
            for i in range(1, len(table2.variables)):
                vs.append(table2.variables[i])
            vs.append(table2.variables[0])
    elif len(table1.variables) == 3 and len(table2.variables) == 7:
        if table1.variables[1] == table2.variables[5] and table1.variables[2] == table2.variables[6] and \
                table1.variables[0] not in [x for x in table2.variables if
                                            x not in [table2.variables[5], table2.variables[6]]]:
            t.append([table2.table[0][0] * table1.table[0][0], table2.table[0][0] * table1.table[0][1]])
            t.append([table2.table[0][1] * table1.table[0][0], table2.table[0][1] * table1.table[0][1]])
            t.append([table2.table[1][0] * table1.table[1][0], table2.table[1][0] * table1.table[1][1]])
            t.append([table2.table[1][1] * table1.table[1][0], table2.table[1][1] * table1.table[1][1]])
            t.append([table2.table[2][0] * table1.table[2][0], table2.table[2][0] * table1.table[2][1]])
            t.append([table2.table[2][1] * table1.table[2][0], table2.table[2][1] * table1.table[2][1]])
            t.append([table2.table[3][0] * table1.table[3][0], table2.table[3][0] * table1.table[3][1]])
            t.append([table2.table[3][1] * table1.table[3][0], table2.table[3][1] * table1.table[3][1]])

            t.append([table2.table[4][0] * table1.table[0][0], table2.table[4][0] * table1.table[0][1]])
            t.append([table2.table[4][1] * table1.table[0][0], table2.table[4][1] * table1.table[0][1]])
            t.append([table2.table[5][0] * table1.table[1][0], table2.table[5][0] * table1.table[1][1]])
            t.append([table2.table[5][1] * table1.table[1][0], table2.table[5][1] * table1.table[1][1]])
            t.append([table2.table[6][0] * table1.table[2][0], table2.table[6][0] * table1.table[2][1]])
            t.append([table2.table[6][1] * table1.table[2][0], table2.table[6][1] * table1.table[2][1]])
            t.append([table2.table[7][0] * table1.table[3][0], table2.table[7][0] * table1.table[3][1]])
            t.append([table2.table[7][1] * table1.table[3][0], table2.table[7][1] * table1.table[3][1]])

            t.append([table2.table[8][0] * table1.table[0][0], table2.table[8][0] * table1.table[0][1]])
            t.append([table2.table[8][1] * table1.table[0][0], table2.table[8][1] * table1.table[0][1]])
            t.append([table2.table[9][0] * table1.table[1][0], table2.table[9][0] * table1.table[1][1]])
            t.append([table2.table[9][1] * table1.table[1][0], table2.table[9][1] * table1.table[1][1]])
            t.append([table2.table[10][0] * table1.table[2][0], table2.table[10][0] * table1.table[2][1]])
            t.append([table2.table[10][1] * table1.table[2][0], table2.table[10][1] * table1.table[2][1]])
            t.append([table2.table[11][0] * table1.table[3][0], table2.table[11][0] * table1.table[3][1]])
            t.append([table2.table[11][1] * table1.table[3][0], table2.table[11][1] * table1.table[3][1]])

            t.append([table2.table[12][0] * table1.table[0][0], table2.table[12][0] * table1.table[0][1]])
            t.append([table2.table[12][1] * table1.table[0][0], table2.table[12][1] * table1.table[0][1]])
            t.append([table2.table[13][0] * table1.table[1][0], table2.table[13][0] * table1.table[1][1]])
            t.append([table2.table[13][1] * table1.table[1][0], table2.table[13][1] * table1.table[1][1]])
            t.append([table2.table[14][0] * table1.table[2][0], table2.table[14][0] * table1.table[2][1]])
            t.append([table2.table[14][1] * table1.table[2][0], table2.table[14][1] * table1.table[2][1]])
            t.append([table2.table[15][0] * table1.table[3][0], table2.table[15][0] * table1.table[3][1]])
            t.append([table2.table[15][1] * table1.table[3][0], table2.table[15][1] * table1.table[3][1]])

            t.append([table2.table[16][0] * table1.table[0][0], table2.table[16][0] * table1.table[0][1]])
            t.append([table2.table[16][1] * table1.table[0][0], table2.table[16][1] * table1.table[0][1]])
            t.append([table2.table[17][0] * table1.table[1][0], table2.table[17][0] * table1.table[1][1]])
            t.append([table2.table[17][1] * table1.table[1][0], table2.table[17][1] * table1.table[1][1]])
            t.append([table2.table[18][0] * table1.table[2][0], table2.table[18][0] * table1.table[2][1]])
            t.append([table2.table[18][1] * table1.table[2][0], table2.table[18][1] * table1.table[2][1]])
            t.append([table2.table[19][0] * table1.table[3][0], table2.table[19][0] * table1.table[3][1]])
            t.append([table2.table[19][1] * table1.table[3][0], table2.table[19][1] * table1.table[3][1]])

            t.append([table2.table[20][0] * table1.table[0][0], table2.table[20][0] * table1.table[0][1]])
            t.append([table2.table[20][1] * table1.table[0][0], table2.table[20][1] * table1.table[0][1]])
            t.append([table2.table[21][0] * table1.table[1][0], table2.table[21][0] * table1.table[1][1]])
            t.append([table2.table[21][1] * table1.table[1][0], table2.table[21][1] * table1.table[1][1]])
            t.append([table2.table[22][0] * table1.table[2][0], table2.table[22][0] * table1.table[2][1]])
            t.append([table2.table[22][1] * table1.table[2][0], table2.table[22][1] * table1.table[2][1]])
            t.append([table2.table[23][0] * table1.table[3][0], table2.table[23][0] * table1.table[3][1]])
            t.append([table2.table[23][1] * table1.table[3][0], table2.table[23][1] * table1.table[3][1]])

            t.append([table2.table[24][0] * table1.table[0][0], table2.table[24][0] * table1.table[0][1]])
            t.append([table2.table[24][1] * table1.table[0][0], table2.table[24][1] * table1.table[0][1]])
            t.append([table2.table[25][0] * table1.table[1][0], table2.table[25][0] * table1.table[1][1]])
            t.append([table2.table[25][1] * table1.table[1][0], table2.table[25][1] * table1.table[1][1]])
            t.append([table2.table[26][0] * table1.table[2][0], table2.table[26][0] * table1.table[2][1]])
            t.append([table2.table[26][1] * table1.table[2][0], table2.table[26][1] * table1.table[2][1]])
            t.append([table2.table[27][0] * table1.table[3][0], table2.table[27][0] * table1.table[3][1]])
            t.append([table2.table[27][1] * table1.table[3][0], table2.table[27][1] * table1.table[3][1]])

            t.append([table2.table[28][0] * table1.table[0][0], table2.table[28][0] * table1.table[0][1]])
            t.append([table2.table[28][1] * table1.table[0][0], table2.table[28][1] * table1.table[0][1]])
            t.append([table2.table[29][0] * table1.table[1][0], table2.table[29][0] * table1.table[1][1]])
            t.append([table2.table[29][1] * table1.table[1][0], table2.table[29][1] * table1.table[1][1]])
            t.append([table2.table[30][0] * table1.table[2][0], table2.table[30][0] * table1.table[2][1]])
            t.append([table2.table[30][1] * table1.table[2][0], table2.table[30][1] * table1.table[2][1]])
            t.append([table2.table[31][0] * table1.table[3][0], table2.table[31][0] * table1.table[3][1]])
            t.append([table2.table[31][1] * table1.table[3][0], table2.table[31][1] * table1.table[3][1]])

            t.append([table2.table[32][0] * table1.table[0][0], table2.table[32][0] * table1.table[0][1]])
            t.append([table2.table[32][1] * table1.table[0][0], table2.table[32][1] * table1.table[0][1]])
            t.append([table2.table[33][0] * table1.table[1][0], table2.table[33][0] * table1.table[1][1]])
            t.append([table2.table[33][1] * table1.table[1][0], table2.table[33][1] * table1.table[1][1]])
            t.append([table2.table[34][0] * table1.table[2][0], table2.table[34][0] * table1.table[2][1]])
            t.append([table2.table[34][1] * table1.table[2][0], table2.table[34][1] * table1.table[2][1]])
            t.append([table2.table[35][0] * table1.table[3][0], table2.table[35][0] * table1.table[3][1]])
            t.append([table2.table[35][1] * table1.table[3][0], table2.table[35][1] * table1.table[3][1]])

            t.append([table2.table[36][0] * table1.table[0][0], table2.table[36][0] * table1.table[0][1]])
            t.append([table2.table[36][1] * table1.table[0][0], table2.table[36][1] * table1.table[0][1]])
            t.append([table2.table[37][0] * table1.table[1][0], table2.table[37][0] * table1.table[1][1]])
            t.append([table2.table[37][1] * table1.table[1][0], table2.table[37][1] * table1.table[1][1]])
            t.append([table2.table[38][0] * table1.table[2][0], table2.table[38][0] * table1.table[2][1]])
            t.append([table2.table[38][1] * table1.table[2][0], table2.table[38][1] * table1.table[2][1]])
            t.append([table2.table[39][0] * table1.table[3][0], table2.table[39][0] * table1.table[3][1]])
            t.append([table2.table[39][1] * table1.table[3][0], table2.table[39][1] * table1.table[3][1]])

            t.append([table2.table[40][0] * table1.table[0][0], table2.table[40][0] * table1.table[0][1]])
            t.append([table2.table[40][1] * table1.table[0][0], table2.table[40][1] * table1.table[0][1]])
            t.append([table2.table[41][0] * table1.table[1][0], table2.table[41][0] * table1.table[1][1]])
            t.append([table2.table[41][1] * table1.table[1][0], table2.table[41][1] * table1.table[1][1]])
            t.append([table2.table[42][0] * table1.table[2][0], table2.table[42][0] * table1.table[2][1]])
            t.append([table2.table[42][1] * table1.table[2][0], table2.table[42][1] * table1.table[2][1]])
            t.append([table2.table[43][0] * table1.table[3][0], table2.table[43][0] * table1.table[3][1]])
            t.append([table2.table[43][1] * table1.table[3][0], table2.table[43][1] * table1.table[3][1]])

            t.append([table2.table[44][0] * table1.table[0][0], table2.table[44][0] * table1.table[0][1]])
            t.append([table2.table[44][1] * table1.table[0][0], table2.table[44][1] * table1.table[0][1]])
            t.append([table2.table[45][0] * table1.table[1][0], table2.table[45][0] * table1.table[1][1]])
            t.append([table2.table[45][1] * table1.table[1][0], table2.table[45][1] * table1.table[1][1]])
            t.append([table2.table[46][0] * table1.table[2][0], table2.table[46][0] * table1.table[2][1]])
            t.append([table2.table[46][1] * table1.table[2][0], table2.table[46][1] * table1.table[2][1]])
            t.append([table2.table[47][0] * table1.table[3][0], table2.table[47][0] * table1.table[3][1]])
            t.append([table2.table[47][1] * table1.table[3][0], table2.table[47][1] * table1.table[3][1]])

            t.append([table2.table[48][0] * table1.table[0][0], table2.table[48][0] * table1.table[0][1]])
            t.append([table2.table[48][1] * table1.table[0][0], table2.table[48][1] * table1.table[0][1]])
            t.append([table2.table[49][0] * table1.table[1][0], table2.table[49][0] * table1.table[1][1]])
            t.append([table2.table[49][1] * table1.table[1][0], table2.table[49][1] * table1.table[1][1]])
            t.append([table2.table[50][0] * table1.table[2][0], table2.table[50][0] * table1.table[2][1]])
            t.append([table2.table[50][1] * table1.table[2][0], table2.table[50][1] * table1.table[2][1]])
            t.append([table2.table[51][0] * table1.table[3][0], table2.table[51][0] * table1.table[3][1]])
            t.append([table2.table[51][1] * table1.table[3][0], table2.table[51][1] * table1.table[3][1]])

            t.append([table2.table[52][0] * table1.table[0][0], table2.table[52][0] * table1.table[0][1]])
            t.append([table2.table[52][1] * table1.table[0][0], table2.table[52][1] * table1.table[0][1]])
            t.append([table2.table[53][0] * table1.table[1][0], table2.table[53][0] * table1.table[1][1]])
            t.append([table2.table[53][1] * table1.table[1][0], table2.table[53][1] * table1.table[1][1]])
            t.append([table2.table[54][0] * table1.table[2][0], table2.table[54][0] * table1.table[2][1]])
            t.append([table2.table[54][1] * table1.table[2][0], table2.table[54][1] * table1.table[2][1]])
            t.append([table2.table[55][0] * table1.table[3][0], table2.table[55][0] * table1.table[3][1]])
            t.append([table2.table[55][1] * table1.table[3][0], table2.table[55][1] * table1.table[3][1]])

            t.append([table2.table[56][0] * table1.table[0][0], table2.table[56][0] * table1.table[0][1]])
            t.append([table2.table[56][1] * table1.table[0][0], table2.table[56][1] * table1.table[0][1]])
            t.append([table2.table[57][0] * table1.table[1][0], table2.table[57][0] * table1.table[1][1]])
            t.append([table2.table[57][1] * table1.table[1][0], table2.table[57][1] * table1.table[1][1]])
            t.append([table2.table[58][0] * table1.table[2][0], table2.table[58][0] * table1.table[2][1]])
            t.append([table2.table[58][1] * table1.table[2][0], table2.table[58][1] * table1.table[2][1]])
            t.append([table2.table[59][0] * table1.table[3][0], table2.table[59][0] * table1.table[3][1]])
            t.append([table2.table[59][1] * table1.table[3][0], table2.table[59][1] * table1.table[3][1]])

            t.append([table2.table[60][0] * table1.table[0][0], table2.table[60][0] * table1.table[0][1]])
            t.append([table2.table[60][1] * table1.table[0][0], table2.table[60][1] * table1.table[0][1]])
            t.append([table2.table[61][0] * table1.table[1][0], table2.table[61][0] * table1.table[1][1]])
            t.append([table2.table[61][1] * table1.table[1][0], table2.table[61][1] * table1.table[1][1]])
            t.append([table2.table[62][0] * table1.table[2][0], table2.table[62][0] * table1.table[2][1]])
            t.append([table2.table[62][1] * table1.table[2][0], table2.table[62][1] * table1.table[2][1]])
            t.append([table2.table[63][0] * table1.table[3][0], table2.table[63][0] * table1.table[3][1]])
            t.append([table2.table[63][1] * table1.table[3][0], table2.table[63][1] * table1.table[3][1]])

            vs = []
            vs.append(table1.variables[0])
            for i in range(1, len(table2.variables)):
                vs.append(table2.variables[i])
            vs.append(table2.variables[0])

    elif (len(table1.variables) == 2 and len(table2.variables) == 1) or (
            len(table1.variables) == 3 and len(table2.variables) == 1) or (
            len(table1.variables) == 3 and len(table2.variables) == 2) or (
            len(table1.variables) == 4 and len(table2.variables) == 2) or (
            len(table1.variables) == 5 and len(table2.variables) == 3) or (
            len(table1.variables) == 6 and len(table2.variables) == 2) or (
            len(table1.variables) == 7 and len(table2.variables) == 3):
        return multiplyBTs(table2, table1)

    return BeliefTable(variables=vs, table=t)


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
                              [[1, 0], [0.1, 0.9], [0.1, 0.9], [0.01, 0.99]]))
    return ts
