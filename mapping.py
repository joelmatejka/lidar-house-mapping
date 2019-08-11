#!/usr/bin/python3

import sys
import math
import numpy as np
from hokuyolx import HokuyoLX
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
import svgwrite

DMAX = 10000
STEPS = [100, 500, 1000, 2000, 5000, 10000]
COLORS = ['#d68080', '#d69580', '#d6ab80', '#d6c080', '#d6d680', '#c0d680', '#abd680', '#95d680', '#80d680', '#80d695', '#80d6ab', '#80d6c0', '#80d6d6', '#80ced6', '#80c0d6', '#80abd6', '#8095d6', '#8080d6', '#9580d6', '#ab80d6', '#c080d6', '#d680d6', '#d680c0', '#d680ab', '#d68095', '#d68080']

def save_svg():
    dwg = svgwrite.Drawing('plan.svg', size=('1000mm', '1000mm'), viewBox=('0 0 1000 1000'))
    counter = 0
    for sample in dataset:
        group = svgwrite.container.Group(id='Scan%d' % counter)
        counter = counter + 1
        for point in sample[1]:
            group.add(dwg.circle(center=(point[0], -point[1]), r=10, stroke=COLORS[counter % len(COLORS)], fill="none", stroke_width=5))
        dwg.add(group)
    dwg.save()

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
    global color_index
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
        plot = ax.plot(*cartesian.T, '.', color=COLORS[color_index])[0]
        color_index = (color_index + 1) % len(COLORS)
        dataset.append([[pos_x, pos_y, orientation], cartesian])
        plt.draw()
        print(dataset)
        save_svg()

# plt.ion()

pos_x = 0
pos_y = 0
step_index = 2
color_index = 0
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
