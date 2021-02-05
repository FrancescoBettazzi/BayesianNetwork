import numpy as np

class BeliefTable(object):

    def __init__(self, name, v=None):
        self.name = name
        self.v = v

    def setTable(self):
        print("Table setted")

    def getName(self):
        return self.name

    def multiply(self, bt1, bt2):
        tmp_bt = BeliefTable(bt1.getName()+bt2.getName())
