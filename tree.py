"""
Transformation tree allows data scientists to build and evaluate multiple pipelines

Parts:
OP_TYPE_TABLE: Stores the type of operator for each func/method
Node: Stores individual operator along with positional and keyword args necessary to execute operator (except for data),
along with references to parent and children nodes. Includes method to execute operator function stored in Node.
Tree: Non-binary tree made up of Nodes. Includes methods to manipulate the tree by adding/removing/changing individual nodes, enforce
compatibility between nodes, execute pipelines in the tree, and write/read trees to/from files.
"""
from copy import deepcopy
from Project1 import *

def report_function(d):
    return print(d.a)
def test_func(f1,f2):
    d = DummyClass(5)
    abc = [1,2,3]
    f1(d, *abc)
    print(d.a)
    

class DummyClass:
    def __init__(self, a):
        self.a = a
    def seta(self, a, b, c):
        self.a = 20*a*b*c
        return None    
    def geta(self):
        return self.able

test_func(DummyClass.seta, DummyClass.geta)


class OP_TYPES:
    INPUT = 0
    OUTPUT = 1
    PREPROCESSING = 2
    MODELING = 3
    FORECASTING = 4
    VISUALIZATION = 5
    ERROR_MEASUREMENT = 6

class Node:
    def __init__(self, operator, args: list, parent=None, children=[]):
        self.operator = operator
        self.args = args
        self.parent = parent
        self.children = children

    def execute(self, data):
        return self.operator(data, *args)



ts = TimeSeries()
