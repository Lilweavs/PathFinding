from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import sys

fig, ax = plt.subplots()
ax.axis('scaled')

width = int(sys.argv[1])
height = int(sys.argv[2])

ax.set_xlim([0, width])
ax.set_ylim([0, height])

Map = np.zeros((height, width))




def onclick(event):

    i = np.floor(event.xdata)
    j = np.floor(event.ydata)

    print(f'X: {np.floor(event.xdata)}, Y: {np.floor(event.ydata)}')

    patches = ax.patches
    
    if len(patches) == 0:
        print('true')
        ax.add_patch(Rectangle((i, j), 1, 1, fc='black'))

    # print(patches)
    pose = np.array([i, j])
    truth_table = [np.array_equal(patch.xy, pose) for patch in patches]

    print(len(patches))

    if not np.any(truth_table):
        ax.add_patch(Rectangle((i, j), 1, 1, fc='black'))



    # for patch in patches:


    #     if np.array_equal(patch.xy, pose):
    #         pass
    #         # print('repeat')
    #     else:
    #         ax.add_patch(Rectangle((i, j), 1, 1, fc='black'))

    ax.figure.canvas.draw()





cid = fig.canvas.mpl_connect('button_release_event', onclick)

plt.show()