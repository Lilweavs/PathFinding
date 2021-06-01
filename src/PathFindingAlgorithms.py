#!/usr/env/bin python
from math import sqrt
from collections import deque
from typing import List, Tuple
from collections import namedtuple
import heapq

from numpy.core.getlimits import _discovered_machar
from numpy.lib.function_base import _parse_input_dimensions

# class Node:
#     def __init__(self, x=0, y=0, parent=[0, 0]):
#         self.x = x
#         self.y = y
#         self.f = 0
#         self.g = 0
#         self.h = 0
#         self.parent = parent

#     def __repr__(self):
#         return f'Location: {self.x},{self.y}, f: {self.f}, g: {self.g}, h: {self.h}, parent: {self.parent}'

class Node:
    def __init__(self, child, parent=(0, 0), f=0, g=0):
        self.child = child
        self.parent = parent
        self.f = f
        self.g = g


class PathFinding:
    
    def __init__(self, Map = [[0]*5]*5, start = (0, 0), goal = (4, 4)):
        self.map = Map
        self.start = start
        self.goal = goal


class Astar(PathFinding):

    def __init__(self, Map, start, goal):
        super().__init__(Map=Map, start=start, goal=goal)
        self.openList = [(0, (Node(self.start)))]
        self.closedList = dict()
        self.dir_l = [( 1, 0), (-1, 0), (0, -1), (0,  1)]

    # calculate f cost
    def get_adjacent(self, node):
        adjacentList = []
        directions = self.dir_l

        for d in directions:
            x = d[0] + node.child[0]
            y = d[1] + node.child[1]
            if not (((x == -1) or (x == len(self.map))) or ((y == -1) or (y == len(self.map[0])))):
                if not self.map[x][y] == 1:

                    if self.map[x][y] == 5:
                        moveCost = 3.5
                    else:
                        moveCost = 1

                    adjacentNode = Node((x, y), node.child)

                    if (node.child[0] + node.child[1]) % 2 == 0 and not x == node.child[0]:
                        tmp = 0.001

                    elif (node.child[0] + node.child[1]) % 2 == 1 and not y == node.child[1]:
                        tmp = 0.001
                    else:
                        tmp = 0.0

                    adjacentNode.g = node.g + moveCost + tmp
                    adjacentNode.f = adjacentNode.g + self.get_heuristic(adjacentNode)
                    adjacentList.append(adjacentNode)

        return adjacentList
    

    def get_heuristic(self, node):
        dx = abs(node.child[0] - self.goal[0])
        dy = abs(node.child[1] - self.goal[1])

        return dx + dy 


    def solve(self) -> list:
            path = []
            while self.openList:
                # currentNode -> tuple = Node(child, x, y)
                cost, currentNode = heapq.heappop(self.openList)
                # print(currentNode)
                if currentNode.child == self.goal:
                    print('A* Found A Path!')
                    # print(f'{self.closedList}')
                    while self.start not in path:
                        path.append(currentNode.child)
                        currentNode = self.closedList[currentNode.parent]
                    return path
                # closedList -> dict = {child1: parent1, child2: parent2 ...}
                # self.closedList.update(currentNode)

                # adjacentNode -> 
                for adjacentNode in self.get_adjacent(currentNode):
                    
                    if adjacentNode.child not in self.closedList:
                        heapq.heappush(self.openList, (adjacentNode.f, (adjacentNode)))
                        self.closedList[adjacentNode.child] = adjacentNode
                    else:
                        if adjacentNode.f < self.closedList[adjacentNode.child].f:
                            self.closedList[adjacentNode.child] = adjacentNode
            
            return path

class Dijkstra(PathFinding):

    def __init__(self, *args):
        super().__init__(*args)
        self.openList = [(0, (self.start))]
        self.closedList = dict({self.start: [self.start, 0]})
        self.dir_l = [( 1, 0), (-1, 0), (0, -1), (0,  1)]


    def get_adjacent(self, node, cost) -> list:
        adjacentList = []

        directions = self.dir_l

        for d in directions:
            x = d[0] + node[0]
            y = d[1] + node[1]
            if not (((x == -1) or (x == len(self.map))) or ((y == -1) or (y == len(self.map[0])))):
                if not self.map[x][y] == 1:

                    if self.map[x][y] == 5:
                        moveCost = 3.5
                    else:
                        moveCost = 1

                    if (node[0] + node[1]) % 2 == 0 and not x == node[0]:
                        tmp = cost + moveCost + 0.001
                        adjacentList.append(((x, y), tmp))
                    elif (node[0] + node[1]) % 2 == 1 and not y == node[1]:
                        tmp = cost + moveCost + 0.001
                        adjacentList.append(((x, y), tmp))
                    else:
                        tmp = cost + moveCost 
                        adjacentList.append(((x, y), tmp))

        return adjacentList

    def move_cost(self, node):
        pass

    def solve(self) -> list:
            path = []
            while self.openList:
                # currentNode -> tuple = ((x, y), cost)
                cost, currentNode = heapq.heappop(self.openList)
                # print(currentNode)
                if currentNode == self.goal:
                    print('Dijkstra Found A Path!')
                    # print(f'{self.closedList}')
                    while self.start not in path:
                        path.append(currentNode)
                        currentNode = self.closedList[currentNode][0]
                    return path
                # closedList -> dict = {child1: parent1, child2: parent2 ...}
                # self.closedList.update(currentNode)

                # adjacentNode -> tuple ((x, y), cost)
                for adjacentNode, ncost in self.get_adjacent(currentNode, cost):
                    
                    if adjacentNode not in self.closedList:
                        self.openList.append((ncost, adjacentNode))
                        self.closedList[adjacentNode] = (currentNode, ncost)
                    else:
                        if ncost < self.closedList[adjacentNode][1]:
                            self.closedList[adjacentNode] = (currentNode, ncost)
            
            return path

 
class BFS(PathFinding):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.openList = deque([self.start])
        self.closedList = dict({self.start: self.start})
        self.dir_l = [( 1, 0), (-1, 0), (0, -1), (0,  1)]
        self.dir_r = [(-1, 0), ( 1, 0), (0,  1), (0, -1)]

    def get_adjacent(self, node) -> list:
        adjacentList = []

        if node[1] < self.goal[1]:
            directions = self.dir_l
        else:
            directions = self.dir_r

        for d in directions:
            x = d[0] + node[0]
            y = d[1] + node[1]
            if not (((x == -1) or (x == len(self.map))) or ((y == -1) or (y == len(self.map[0])))):
                if not self.map[x][y] == 1:
                    adjacentList.append((x, y))
            if (node[0] + node[1]) % 2 == 0:
                adjacentList.reverse()

        return adjacentList
    
    def solve(self) -> list:
        path = []
        while self.openList:
            # currentNode -> tuple = (x, y)
            currentNode = self.openList.popleft()
            # print(currentNode)
            if currentNode == self.goal:
                print('BFS Found A Path!')
                # print(f'{self.closedList}')
                while self.start not in path:
                    path.append(currentNode)
                    currentNode = self.closedList[currentNode]
                return path
            # closedList -> dict = {child1: parent1, child2: parent2 ...}
            # self.closedList.update(currentNode)

            # adjacentNode -> tuple (x, y)
            for adjacentNode in self.get_adjacent(currentNode):
                
                if adjacentNode not in self.closedList:
                    self.openList.append(adjacentNode)
                    self.closedList[adjacentNode] = currentNode
        
        return path