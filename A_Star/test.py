from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys
global ax, start, end
fig, ax = plt.subplots()
ax.axis('scaled')

width = int(sys.argv[1])
height = int(sys.argv[2])

ax.set_xlim([0, width])
ax.set_ylim([0, height])

Map = np.zeros((height, width))

color = 'blue'

# ax.add_patch(Rectangle((0, 0), 1, 1, fc='blue',picker=True))

obsticles = []
start = Rectangle((0, 0), 1, 1, fc='blue', picker=True)
end = Rectangle((9, 9), 1, 1, fc='green', picker=True)
ax.add_patch(start)
ax.add_patch(end)


def onClick(event):
    global ax, start, end

    i = np.floor(event.xdata)
    j = np.floor(event.ydata)

    if (event.inaxes == ax) and (event.button == 1):

        if color == 'blue':
            start.remove()
            start = Rectangle((i, j), 1, 1, fc=color)
            ax.add_patch(start)
            ax.figure.canvas.draw()
        elif color == 'green':
            end.remove()
            end = Rectangle((i, j), 1, 1, fc=color)
            ax.add_patch(end)
            ax.figure.canvas.draw()


            print(f'X: {np.floor(event.xdata)}, Y: {np.floor(event.ydata)}')

            patches = ax.patches
            
            if len(patches) == 0:
                rect = Rectangle((i, j), 1, 1, fc=color, picker=True)
                obsticles.append(rect)
                ax.add_patch(rect)

            # print(patches)
            pose = np.array([i, j])
            truth_table = [np.array_equal(patch.xy, pose) for patch in patches]

            print(event)

            if not np.any(truth_table):
                rect = Rectangle((i, j), 1, 1, fc=color, picker=True)
                obsticles.append(rect)
                ax.add_patch(rect)

        
            elif (event.inaxes == ax) and (event.button == 3):

                obsticles[-1].remove()
                obsticles.pop()

    ax.figure.canvas.draw()

def onPick(event):
    global ax
    print(event)
    # print(event.artist)
    event.artist.remove()
    ax.figure.canvas.draw()
    # print(event.artist)

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
plt.subplots_adjust(left=0.3)
axcolor = 'lightgoldenrodyellow'
rax = plt.axes([0.05, 0.7, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('Start', 'End', 'Obs'))

def do(label):
    global color
    if label == "Start":
        color = 'blue'
    elif label == "End":
        color = 'green'
    else:
        color = 'black'


radio.on_clicked(do)

cid = fig.canvas.mpl_connect('button_press_event', onClick)
# cid2 = fig.canvas.mpl_connect('pick_event', onPick)

plt.show()