class Cluster(object):
    def __init__(self, variables, table, neighbours=None, separator=False):
        # variables = a list of strings(name of Cluster)
        # table = a belief table
        # neighbours = a list of Clusters
        # separator = boolean
        self.variables = variables
        self.separator = separator
        self.neighbours = neighbours
        self.table = table


class JunctionTree(object):
    def __init__(self, clusters=None):
        # clusters = a list of Clusters
        self.clusters = clusters

    def addCluster(self, variables, table, neighbours=None, separator=False):
        # variables = a list of strings (name of Cluster)
        # table = a belief table
        # neighbours = a list of list of strings(representing clusters)
        # separator = boolean
        for c in self.clusters:
            if len(set(c.variables).intersection(variables)) == len(variables):
                print('Cluster già contenuto')
                return False
        if neighbours != None:
            ns = []
            for c in self.clusters:
                if c.name in neighbours:
                    ns.append(c)
        else:
            ns = None
        new = Cluster(variables=variables, table=table, neighbours=ns,
                      separator=separator)
        self.clusters.append(new)
