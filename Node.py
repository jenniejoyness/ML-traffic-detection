"""
The class creates Nodes for the decision
tree of ID3 class.
"""


class Node:
    def __init__(self, att_name, values=None):
        self.att_name = att_name
        self.values = values
