#!/usr/env/bin python

import node as n
import numpy as np

class A_star:
    def __init__(self):
        self.start_node = np.array([0, 0])
        self.end_node = np.array([9, 9])
        self.open_list = np.array([], dtype=object)
        self.closed_list = np.array([], dtype=object)
        self.curr_list = np.array([], dtype=object)
        self.open_list = np.append(self.open_list, n.Node(self.start_node))
        self.node_gen = np.array([[-1, -1 ],
                                  [-1,  0 ],
                                  [-1,  1 ],
                                  [ 0, -1 ],
                                  [ 0,  1 ],
                                  [ 1, -1 ],
                                  [ 1,  0 ],
                                  [ 1,  1 ]])
        self.map = n.Map()

    def gen_adjacent_nodes(self, node):
        nodeList = self.node_gen + node.loc
        
        self.curr_list = np.array([], dtype=object)

        for i, tmp in enumerate(nodeList):
            if (not ((tmp == -1).any())) and not ((tmp == self.map.size[0]).any()):
                if not (self.map.map[tmp[0], tmp[1]] == 1):
                    self.curr_list = np.append(self.curr_list, n.Node(loc=tmp, parent=node.loc))
            else:
                pass
                # print(tmp)

    def loop(self):

        # while not self.open_list.size == 0:
        for k in range(9):
            min_f = 1e4
            index = 0

            for i, node in enumerate(self.open_list):
                if (node.f < min_f):
                    index = i
                    min_f = node.f

            q = self.open_list[index]

            if np.array_equal(q.loc, self.end_node):
                print('finished')

            print(f'Chosen node: {q}')
            self.open_list = np.delete(self.open_list, index)
            self.closed_list = np.append(self.closed_list, q)
            self.gen_adjacent_nodes(q)

            for i, node in enumerate(self.curr_list):

                if self.find(node, 1):
                    print('Ignore: In closed list')
                    continue

                node.g = q.g + np.sum((node.loc - q.g)**2)
                node.h = np.sum((node.loc - self.end_node)**2)
                node.f = node.g + node.h
                
                there, idx = self.find(node, 0)
                if there:
                    print('In open list')
                    if node.g > self.open_list[idx].g:
                        continue
                    else:
                        self.open_list[idx].parent = q.loc
                        self.open_list[idx].g = q.g + np.sum((self.open_list[idx].loc - self.start_node)**2)#self.open_list[idx].parent)**2)
                        self.open_list[idx].f = self.open_list[idx].g + self.open_list[idx].h
                else:
                    self.open_list = np.append(self.open_list, node)
            
                

                # elif not (tmp[0]):
                #         node.added(sn=self.start_node, en=self.end_node, parent=q.loc)

                #         print("Added to open list")
                # else:
                #     if self.open_list[tmp[1]].g < q.g:
                #         print("better")


            print("Open List")
            for i, node in enumerate(self.open_list):

                print(node)
            print("Closed List")
            for i, node in enumerate(self.closed_list):
                print(node)
            print()

    def find(self, node, flag):
        if flag == 0:
            for i, _node in enumerate(self.open_list):
                if np.array_equal(node.loc, _node.loc):
                    return True, i
            return False, 0
        else:
            for i, _node in enumerate(self.closed_list):
                if np.array_equal(node.loc, _node.loc):
                    return True
            return False

def main():
    pathFinder = A_star()

    pathFinder.loop()

if __name__ == "__main__":
    main()