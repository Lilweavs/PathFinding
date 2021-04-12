#!/usr/env/bin python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle

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
    #     self.rect = []
    #     self.size = size
    #     self.generate()

    # def generate(self):
    #     for i, row in enumerate(self.map):
    #         print(row)
    #         for j, col in enumerate(row):
    #             if col == 1:
    #                 self.ax.add_patch(Rectangle((i, j), 1, 1, fc='black'))
    #     plt.axis('scaled')
    #     plt.xlim([0, 10])
    #     plt.ylim([0, 10])
    #     plt.show()
        # rectangle1 = Rectangle((0, 0), 1, 1, fc='black')


# if __name__ == "__main__":


# print(n.map)

# print(n.map)

# width = 10
# height = 10

# x = np.arange(10)
# y = np.arange(10)

# fig = plt.figure()
# ax = fig.add_subplot(111)

# for i in range(len(x)):
#     plt.axhline(y[i], color='k')
#     plt.axvline(x[i], color='k')

# plt.axis('scaled')
# plt.xlim([0, 10])
# plt.ylim([0, 10])

# plt.show()

# freqs = np.arange(2, 20, 3)

# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.2)
# t = np.arange(0.0, 1.0, 0.001)
# s = np.sin(2*np.pi*freqs[0]*t)
# l, = plt.plot(t, s, lw=2)

# class Index(object):
#     ind = 0

#     def next(self, event):
#         self.ind += 1
#         i = self.ind % len(freqs)
#         ydata = np.sin(2*np.pi*freqs[i]*t)
#         l.set_ydata(ydata)
#         plt.draw()

#     def prev(self, event):
#         self.ind -= 1
#         i = self.ind % len(freqs)
#         ydata = np.sin(2*np.pi*freqs[i]*t)
#         l.set_ydata(ydata)
#         plt.draw()

# callback = Index()
# axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
# bnext = Button(axnext, 'Next')
# bnext.on_clicked(callback.next)
# bprev = Button(axprev, 'Previous')
# bprev.on_clicked(callback.prev)

# plt.show()