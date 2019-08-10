#!/usr/bin/python3

import sys
import math
import numpy as np
from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow

DMAX = 10000

def update_arrow():
    global arrow
    arrow.remove()
    arrow_obj = Arrow(pos_x, pos_y, 0, orientation*1000, width=200, color="red")
    arrow = ax.add_patch(arrow_obj)
    ax.set_xlim(-DMAX + pos_x, DMAX + pos_x)
    ax.set_ylim(-DMAX + pos_y, DMAX + pos_y)
    plt.draw()

def press(event):
    global pos_x
    global pos_y
    global orientation
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'up':
        pos_y = pos_y + 100
        update_arrow()
    if event.key == 'down':
        pos_y = pos_y - 100
        update_arrow()
    if event.key == 'left':
        pos_x = pos_x - 100
        update_arrow()
    if event.key == 'right':
        pos_x = pos_x + 100
        update_arrow()
    if event.key == 'o':
        orientation = orientation * -1
        update_arrow()
    if event.key == 'x':
        timestamp, scan = laser.get_filtered_dist(dmax=DMAX)

        cartesian = np.array([[-orientation * distance * math.cos(angle-math.pi/2), -orientation * distance * math.sin(angle-math.pi/2)] for (angle, distance) in scan])
        cartesian = cartesian + np.array([pos_x, pos_y])
        print(cartesian)
        plot.set_data(*cartesian.T)
        text.set_text('t: %d' % timestamp)
        plt.draw()

#plt.ion()

pos_x = 0
pos_y = 0

orientation = 1

laser = HokuyoLX()
fig, ax = plt.subplots()
plot = ax.plot([], [], '.')[0]
arrow_obj = Arrow(pos_x, pos_y, 0, orientation*1000, width=200, color="red")
arrow = ax.add_patch(arrow_obj)
text = plt.text(0, 1, '', transform=ax.transAxes)
ax.set_xlim(-DMAX,DMAX)
ax.set_ylim(-DMAX,DMAX)
ax.grid(True)
fig.canvas.mpl_connect('key_press_event', press)
plt.draw()
plt.show()
laser.close()