import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from matplotlib.colors import ListedColormap, BoundaryNorm
import functools
from math import floor
import numpy as np
from src.PathFindingAlgorithms import BFS, Dijkstra


class PathGUI():
    
    def __init__(self, Map, pathFinderType='BFS'):
        """
        Constructor to initialize GUI

        arguments:
            Map: 2D numpy array of a map

            pathFinder: a path finding algorithm class

        parameters:

            path: list to store path return by path finding algorithms

            clicked: true if mouse is clicked

            inAxis: true if mouse is in the plotting area

        """

        self.path = []
        self.clicked = False
        self.inAxis = False

        """
        Visualization Settings

        """
        self.fig, self.ax = plt.subplots(figsize=(10,5), dpi=200)
        self.ax.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
        self.colors ={'blank': (0, 'white'), 'Wall': (1, '#312F2F'), 'Start': (2, '#3666BF'), 'End': (3, 'green'), 'Visit': (4, 'grey')}
        self.type = 'Start'

        cmap = ListedColormap([self.colors[i][1] for i in self.colors])
        bounds = BoundaryNorm([0, 1, 2, 3, 4, 5], cmap.N) 
        cmap.set_under(color='w', alpha=0)
        
        self.fig.subplots_adjust(left=0.2)
        self.bkg = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        self.radio_axis = self.fig.add_axes([0.05, 0.4, 0.1, 0.2])
        self.radio = RadioButtons(self.radio_axis, ('Start', 'End', 'Wall'))
        self.radio.on_clicked(self.set_color)

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("axes_enter_event", self.on_enter)
        self.fig.canvas.mpl_connect("axes_leave_event", self.on_leave)

        """
        Initial Map Settings
        
        parameters:

            pathFinder: path finding algorithm -> BFS is the default

            start: location of starting node -> tuple

            goal: location of goal node -> tuple

            row: store height of map -> int (only used to fix bug when creating nodes at the top of the map)

        """
        self.pathFinderType = pathFinderType
        self.map = np.flip(np.array(Map), axis=0)
        self.row = len(self.map[0]) - 1
        self.col = len(self.map) - 1
        self.start = (0, 0)
        self.goal = (self.col, self.row)

        self.map[self.start] = 2
        self.map[self.goal] = 3

        
        self.maze = self.ax.pcolormesh(self.map, edgecolors='black', norm=bounds, cmap=cmap)
        self.ax.axis('scaled')
        

    def on_move(self, event):
        if self.clicked and self.inAxis:
            self.wallHandle(event)


    def wallHandle(self, event):
        tmp = (floor(event.ydata), floor(event.xdata))

        if tmp[0] > self.col:
            tmp = (self.col, tmp[1])

        if event.button == 1:
            if self.type == 'Start':
                if not ((tmp == self.goal) or (self.map[tmp] == 1) or (self.map[tmp] == 2)):
                    self.map[self.start] = 0
                    self.start = tmp
                    self.map[self.start] = self.colors['Start'][0]

            elif self.type == 'End':
                if not ((tmp == self.start) or (self.map[tmp] == 1)):
                    self.map[self.goal] = 0
                    self.goal = tmp
                    self.map[self.goal] = self.colors['End'][0]
            else:
                if not (tmp == self.start or tmp == self.goal):
                    self.map[tmp] = self.colors['Wall'][0]
        else:
            if not (tmp == self.start or tmp == self.goal):
                self.map[tmp] = 0

        self.update()


    def update(self):
        # self.maze.set_data(self.map)
        self.maze.set_array(self.map.flatten())
        # restore background
        self.fig.canvas.restore_region(self.bkg)
        # redraw just the points
        self.ax.draw_artist(self.maze)
        # fill in the axes rectangle
        self.fig.canvas.blit(self.ax.bbox)
        # self.fig.canvas.draw()


    def on_click(self, event):
        if self.inAxis:
            self.clicked = True
            self.wallHandle(event)


    def on_release(self, event):
        self.clicked = False
        if self.inAxis:

            for node in self.path:
                if not self.map[node] == 1:
                    self.map[node] = 0

            if self.pathFinderType == 'BFS':
                self.pathFinder = BFS(self.map, self.start, self.goal)
            elif self.pathFinderType == 'Dij':
                self.pathFinder = Dijkstra(self.map, self.start, self.goal)
            else:
                pass
                # self.pathFinderType == astar(self.map, self.start, self.goal)


            # self.pathFinder = BFS(self.map, self.start, self.goal)
            # self.pathFinder = self.pathFinder(self.map, self.start, self.goal)

            self.path = self.pathFinder.solve()

            if self.path:
                del self.path[0]
                del self.path[-1]
                for node in self.path:
                    self.map[node] = 4
            else:
                print('no path')

        self.update()


    def on_enter(self, event):
        if event.inaxes == self.ax:
            self.inAxis = True


    def on_leave(self, event):
        self.inAxis = False


    def set_color(self, event):
        self.type = event