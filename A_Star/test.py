from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys






global ax, start, end, Map
fig, ax = plt.subplots()
ax.axis('scaled')

width = 20
height = 20

ax.set_xlim([0, width])
ax.set_ylim([0, height])

Map = np.zeros((height , width))

color = 'blue'

# ax.add_patch(Rectangle((0, 0), 1, 1, fc='blue',picker=True))

obs = []
start = Rectangle((0, 0), 1, 1, fc='blue', picker=True)
end = Rectangle((9, 9), 1, 1, fc='green', picker=True)
ax.add_patch(start)
ax.add_patch(end)

def onClick(event):
    global ax, start, end

    i = np.floor(event.xdata)
    j = np.floor(event.ydata)

    pose = np.array([i, j])

    if (event.inaxes == ax):
        if (event.button == 1):
            if color == 'black':
                if len(obs) == 0:
                    rect = Rectangle(pose, 1, 1, fc=color)
                    obs.append(rect)
                    ax.add_patch(rect)
                else:
                    tTable = [np.array_equal(pose, rect.xy) for rect in obs]

                    if not tTable.count(True):
                        rect = Rectangle(pose, 1, 1, fc=color)
                        obs.append(rect)
                        ax.add_patch(rect)

            elif color == 'blue':
                start.remove()
                start = Rectangle(pose, 1, 1, fc=color)
                ax.add_patch(start)
            else:
                end.remove()
                end = Rectangle(pose, 1, 1, fc=color)
                ax.add_patch(end)
        
        elif (event.button == 3):

            if len(obs) == 0:
                pass
            else:

                for idx, rect in enumerate(obs):
                    if np.array_equal(pose, rect.xy):
                        rect.remove()
                        obs.pop(idx)

    ax.figure.canvas.draw()

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


def setMap(event):
    global ax, Map
    ax.set_title('Working')
    # plt.title('Working!!')
    ax.figure.canvas.draw()

    for rect in obs:
        i, j = [int(x) for x in rect.xy]
        Map[j, i] = 1

    print(Map)




def runAstar(event):
    pass

axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(setMap)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(runAstar)






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

plt.show()





if __name__ == "__main__":

    pass