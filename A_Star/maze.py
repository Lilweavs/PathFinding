#!/usr/env/bin python

import node as n
from numpy import array
import matplotlib.pyplot as plt

"""
clear A_star after loop call

print(Start, end location)

change name conventions and fix class system

add vizualizations


"""

class astar:

    def __init__(self, start, end, _map):
        self.start = start
        self.end = end
        self.open_list = []
        self.closed_list = []
        self.adjacent_list = []
        self.map = _map
        
    def reset(self):
        self.open_list = []
        self.closed_list = []
        self.adjacent_list = []

    def initialize(self, start, end, Map):
        self.map = Map
        self.start_node = array(start)
        self.end_node = array(end)
        self.open_list = np.append(self.open_list, n.Node(self.start_node, parent=self.start_node))

    def gen_adjacent_nodes(self, node):

        self.adjacent_list = []

        loc = node.loc

        for i in range(-1, 2):
            for j in range(-1, 2):
                

        for loc in node_loc:
            if  ((loc[0] >= 0) and (loc[1] >= 0) and (loc[0] < self.map.shape[0]) and (loc[1] < self.map.shape[1])):
                if not (self.map[loc[0], loc[1]] == 1):
                    self.adjacent_list = np.append(self.adjacent_list, n.Node(loc=loc, parent=node.loc))

    def iterate(self):
        
        if not self.open_list.size == 0:
        # while k in range(6):
            min_f = 0
            index = []
            # In open_list find the lowest "F" value
            for i, node in enumerate(self.open_list):
                if (node.f > min_f):
                    index = i
                    min_f = node.f

            explore = []
            hmin = []
            index = []
            for i, node in enumerate(self.open_list):
                if node.f == min_f:
                    index.append(i)
                    hmin.append(node.h)
                    explore.append(node)
            
            idx = hmin.index(min(hmin))

            # Index all nodes with min_f so that they are all explored
                
            current_node = self.open_list[index[idx]]
            self.current_node = current_node
            if np.array_equal(current_node.loc, self.end_node):
                print('done')
                print(f'Current Node {current_node}')
                return

            # if np.array_equal(q.loc, self.end_node):
            #     print('finished')

            #Put visited node on the closed list and then generate adjacent nodes
            print(f'Chosen node: {current_node}')
            self.open_list = np.delete(self.open_list, index)
            self.closed_list = np.append(self.closed_list, current_node)
            self.gen_adjacent_nodes(current_node)

            ## Logic for adjacent nodes
            for adjacent_node in self.adjacent_list:

                if self.inClosed(adjacent_node):
                    print('Ignore: In closed list')
                    continue
                # Heuristic functions

                # Set node cost parameters f, g, h
                adjacent_node.g = current_node.g + 1 #np.linalg.norm(adjacent_node.loc - current_node.loc)**2
                adjacent_node.h = self.heuristic(current_node)
                adjacent_node.f = adjacent_node.g + adjacent_node.h
                
                exists, idx = self.inOpen(adjacent_node)
                if exists:
                    print('In open list')
                    if adjacent_node.g > self.open_list[idx].g:
                        continue
                    else:
                        self.open_list[idx].parent = current_node.loc
                        self.open_list[idx].g = current_node.g + 1 # np.linalg.norm(self.open_list[idx].loc - current_node.loc)**2#self.open_list[idx].parent)**2)
                        self.open_list[idx].h = self.heuristic(self.open_list[idx])
                        self.open_list[idx].f = (self.open_list[idx].g + self.open_list[idx].h)
                else:
                    self.open_list = np.append(self.open_list, adjacent_node)
            
            print("Open List")
            for i, node in enumerate(self.open_list):

                print(node)
            print("Closed List")
            for i, node in enumerate(self.closed_list):
                print(node)
            print()


    def inOpen(self, node):
        for i, _node in enumerate(self.open_list):
            if np.array_equal(node.loc, _node.loc):
                return True, i
        return False, 0

    def inClosed(self, node):
        for i, _node in enumerate(self.closed_list):
            if np.array_equal(node.loc, _node.loc):
                return True
        return False       

    def heuristic(self, node):
        D = 1
        D2 = np.sqrt(2)
        dx = abs(node.loc[0] - self.end_node[0])
        dy = abs(node.loc[1] - self.end_node[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
if __name__ == "__main__":
    astar = A_star()
    maze = n.Maze(10, 20, astar)

    


    plt.show()
