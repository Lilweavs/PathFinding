#!/usr/env/bin python

from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, loc, parent=np.array([0, 0])):
        self.loc = loc
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = parent

    def __repr__(self):
        return f'Loc: {self.loc}, f: {self.f}, g: {self.g}, h: {self.h}, parent: {self.parent}'

    def added(self, sn, en, parent):
        self.g = np.sum((sn - self.loc)**2)
        self.h = np.sum((en - self.loc)**2)
        self.f = self.g + self.h
        self.parent = parent


class Maze:

    def __init__(self, rows, cols, astar):
        self.cols = cols
        self.rows = rows
        self.start = Rectangle((0, 0), 1, 1, fc='blue', picker=True)
        self.end = end = Rectangle((cols-1, rows-1), 1, 1, fc='green', picker=True)
        self.fig, self.ax = plt.subplots(figsize=(5,4), dpi=200)
        self.fig.tight_layout()
        self.map = np.zeros((cols, rows))
        self.color = 'blue'
        self.obs = []
        self.solver = astar
        self.setGrid()

    def setGrid(self):
        self.ax.axis('scaled')
        self.ax.set_xlim([0, self.cols])
        self.ax.set_ylim([0, self.rows])
        self.ax.add_patch(self.start)
        self.ax.add_patch(self.end)
        self.fig.subplots_adjust(left=0.2)

        # axcolor = 'lightgoldenrodyellow'
        self.radio_axis = plt.axes([0.05, 0.4, 0.1, 0.2])
        self.radio_axis.axis('scaled')
        self.button1_axis = plt.axes([0.05, 0.65, 0.1, 0.075])
        # button2_axis = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.radio = RadioButtons(self.radio_axis, ('Start', 'End', 'Obs'))
        self.radio.on_clicked(self.setColor)
  
        self.bnext = Button(self.button1_axis, 'Run')
        self.bnext.on_clicked(self.setMap)
        # bprev = Button(axprev, 'Previous')
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        size = self.fig.get_size_inches()
        print(size)
        # bprev.on_clicked(runAstar)

    def onClick(self, event):

        i = np.floor(event.xdata)
        j = np.floor(event.ydata)

        pose = np.array([i, j])

        if (event.inaxes == self.ax):
            if (event.button == 1):
                if self.color == 'black':
                    if len(self.obs) == 0:
                        rect = Rectangle(pose, 1, 1, fc=self.color)
                        self.obs.append(rect)
                        self.ax.add_patch(rect)
                    else:
                        tTable = [np.array_equal(pose, rect.xy) for rect in self.obs]

                        if not tTable.count(True):
                            rect = Rectangle(pose, 1, 1, fc=self.color)
                            self.obs.append(rect)
                            self.ax.add_patch(rect)

                elif self.color == 'blue':
                    self.start.remove()
                    self.start = Rectangle(pose, 1, 1, fc=self.color)
                    self.ax.add_patch(self.start)
                else:
                    self.end.remove()
                    self.end = Rectangle(pose, 1, 1, fc=self.color)
                    self.ax.add_patch(self.end)
            
            elif (event.button == 3):

                if len(self.obs) == 0:
                    pass
                else:
                    for idx, rect in enumerate(self.obs):
                        if np.array_equal(pose, rect.xy):
                            rect.remove()
                            self.obs.pop(idx)

        self.ax.figure.canvas.draw()

    def setMap(self, event):
        for rect in self.obs:
            i, j = [int(x) for x in rect.xy]
            self.map[i, j] = 1
        self.solver.map = self.map
        self.solver.start_node = np.array(self.start.xy)
        self.solver.end_node = np.array(self.end.xy)
        self.solver.loop()
        # print(self.map)

    def setColor(self, label):
        if label == "Start":
            self.color = 'blue'
        elif label == "End":
            self.color = 'green'
        else:
            self.color = 'black'

class Map:
    def __init__(self, size=(10, 10)):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        # self.map = np.random.randint(2, size=(10, 10))
        self.size = size
        self.map = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                             [0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
                             [1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                             [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                             [1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                             [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 1, 0, 0, 0]])
        self.map = np.zeros((10,10))
        self.map = np.array([[0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0]])
        self.size = self.map.shape