#!/usr/env/bin python

import node as n
import numpy as np

class A_star:
    def __init__(self):
        self.start_node = np.array([0, 0])
        self.end_node = (10, 10)
        self.open_list = np.array([], dtype=object)
        self.closed_list = np.array([], dtype=object)
        self.open_list = np.append(self.open_list, n.Node(self.start_node))
        self.node_gen = np.array([[-1, -1 ],
                                  [-1,  0 ],
                                  [-1,  1 ],
                                  [ 0, -1 ],
                                  [ 0,  0 ],
                                  [ 0,  1 ],
                                  [ 1, -1 ],
                                  [ 1,  0 ],
                                  [ 1,  1 ]])

    def gen_adjacent_nodes(self, node):
        nodeList = self.node_gen + node.loc

        for i, tmp in enumerate(nodeList):
            if not (tmp == -1).any():
                self.open_list = np.append(self.open_list, n.Node(loc=tmp, sn=self.start_node, en=self.end_node, parent=node.loc))



        pass

    def loop(self):
        q = self.open_list[-1]
        self.open_list = np.delete(self.open_list, -1)

        self.gen_adjacent_nodes(q)


def main():
    # initialize first node
    pass


if __name__ == "__main__":
    main()