import bnlearn


def conditionedProb(U, Q, E):
    cpds = U.model.cpds
    for i in cpds:
        if i.variable in E.keys():
            if E.get('asia') == 0:
                i.values[0] = 0
            else:
                i.values[1] = 0
    num = 0
    for i in cpds:
        if i.variable not in Q.keys() and i.variable not in E.keys():
            num = num + i.values

    den = 0
    for i in cpds:
        if i.variable not in E.keys():
            den = den + i.values

    return num / den
