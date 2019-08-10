#!/usr/bin/python3

import sys
import math
import numpy as np
from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow

DMAX = 10000
STEPS = [100, 500, 1000, 2000, 5000, 10000]

def update_arrow():
    global arrow
    arrow.remove()
    arrow_obj = Arrow(pos_x, pos_y, 1000 * math.sin(orientation), 1000 * math.cos(orientation), width=200, color="red")
    arrow = ax.add_patch(arrow_obj)
    ax.set_xlim(-DMAX + pos_x, DMAX + pos_x)
    ax.set_ylim(-DMAX + pos_y, DMAX + pos_y)
    plt.draw()

def update_text():
    text.set_text('x: %d y: %d step = %d' % (pos_x, pos_y, STEPS[step_index]))
    plt.draw()

def press(event):
    global pos_x
    global pos_y
    global orientation
    global step_index
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'up':
        pos_y = pos_y + STEPS[step_index]
        update_arrow()
        update_text()
    if event.key == 'down':
        pos_y = pos_y - STEPS[step_index]
        update_arrow()
        update_text()
    if event.key == 'left':
        pos_x = pos_x - STEPS[step_index]
        update_arrow()
        update_text()
    if event.key == 'right':
        pos_x = pos_x + STEPS[step_index]
        update_arrow()
        update_text()
    if event.key == 'o':
        orientation = (orientation + math.pi / 2) % (2 * math.pi)
        update_arrow()
        update_text()
    if event.key == 'j':
        step_index = (step_index + 1) % len(STEPS)
        update_text()
    if event.key == 'x':
        timestamp, scan = laser.get_filtered_dist(dmax=DMAX)

        cartesian = np.array([[distance * math.cos(angle - orientation - 3 * math.pi / 2),
                               distance * math.sin(angle - orientation - 3 * math.pi / 2)]
                               for (angle, distance) in scan])
        cartesian = cartesian + np.array([pos_x, pos_y])
        plot = ax.plot(*cartesian.T, '.')[0]
        dataset.append([[pos_x, pos_y, orientation], cartesian])
        plt.draw()
        print(dataset)

# plt.ion()

pos_x = 0
pos_y = 0
step_index = 2
orientation = 0

dataset = []

laser = HokuyoLX()
fig, ax = plt.subplots()
arrow_obj = Arrow(pos_x, pos_y, 1000 * math.sin(orientation), 1000 * math.cos(orientation), width=200, color="red")
arrow = ax.add_patch(arrow_obj)
text = plt.text(0, 1, 'x: %d y: %d step = %d' % (pos_x, pos_y, STEPS[step_index]), transform=ax.transAxes)
ax.set_xlim(-DMAX, DMAX)
ax.set_ylim(-DMAX, DMAX)
ax.grid(True)
fig.canvas.mpl_connect('key_press_event', press)
plt.draw()
plt.show()
laser.close()
