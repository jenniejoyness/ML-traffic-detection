"""
The class creates Edges for the decision
tree of ID3 class.
"""


class Edge:
    def __init__(self, value_name, next=None):
        self.value_name = value_name
        self.next = next
