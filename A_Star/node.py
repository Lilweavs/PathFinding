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
        self.g = np.linalg.norm(sn - self.loc)**2
        self.h = np.linalg.norm(en - self.loc)**2
        self.f = int(self.g + self.h)
        self.parent = parent


class Maze:

    def __init__(self, rows, cols, astar):
        self.cols = cols
        self.rows = rows
        self.start = Rectangle((0, 0), 1, 1, fc='blue', picker=True)
        self.end = Rectangle((cols-1, rows-1), 1, 1, fc='green', picker=True)
        self.visited = []
        self.notVisited = []


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
        self.fig.subplots_adjust(left=0.2)

        # self.fig.canvas.draw()

        # axcolor = 'lightgoldenrodyellow'
        self.radio_axis = plt.axes([0.05, 0.4, 0.1, 0.2])
        self.radio_axis.axis('scaled')
        self.button1_axis = plt.axes([0.05, 0.65, 0.1, 0.075])
        self.button2_axis = plt.axes([0.05, 0.3, 0.1, 0.075])
        # button2_axis = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.radio = RadioButtons(self.radio_axis, ('Start', 'End', 'Obs'))
        self.radio.on_clicked(self.setColor)


        self.bnext = Button(self.button1_axis, 'Step')
        self.bnext.on_clicked(self.Step)
        self.bprev = Button(self.button2_axis, 'Load')
        self.bprev.on_clicked(self.setMap)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        # size = self.fig.get_size_inches()
        # print(size)
        # bprev.on_clicked(runAstar)
        start = self.ax.add_patch(self.start)
        end = self.ax.add_patch(self.end)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)


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
        self.solver.reset()
        for rect in self.obs:
            i, j = [int(x) for x in rect.xy]
            self.map[i, j] = 1
        self.solver.initialize(self.start.xy, self.end.xy, self.map)
        print('Map Loaded')
        # self.solve()


    def Step(self, event):

        self.solver.iterate()
        self.onIter()
    
        # while not len(self.solver.open_list) == 0:
        #     self.solver.iterate()
        #     if np.array_equal(self.solver.current_node.loc ,self.end.xy):
        #         print('done')
        #         break
        #     self.onIter()


    def onIter(self):

        if not len(self.visited) == 0:
            for patch in self.visited:
                patch.remove()        
            self.visited = []

        for node in self.solver.open_list:
            rect = Rectangle((node.loc), 1, 1, fc='lightsteelblue')
            # text = plt.text(node.loc[0], node.loc[1], str(node.f))
            self.ax.annotate(f'{node.f}', xy=(rect.get_x(), rect.get_y()), ha='center', textcoords='offset points', xytext=(7,5), fontsize=4)
            self.visited.append(rect)
            # self.ax.add_patch(text)
            self.ax.add_patch(rect)
            self.ax.draw_artist(rect)
            # self.ax.draw_artist(text)

        if not len(self.notVisited) == 0:
            for patch in self.notVisited:
                patch.remove()
            self.notVisited = []
        
        for node in self.solver.closed_list:
            rect = Rectangle((node.loc), 1, 1, fc='lightgreen')
            self.notVisited.append(rect)
            self.ax.add_patch(rect)
            self.ax.draw_artist(rect)

        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.restore_region(self.bg)
        # self.ax.figure.canvas.draw()

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