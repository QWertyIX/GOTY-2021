#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from math import cos, sin

walls = [[[0, 0], [0, 6]],
         [[0, 6], [6, 6]],
         [[6, 6], [6, 1]],
         [[7, 0], [0, 0]],

         [[1, 0], [1, 1]],
         [[1, 1], [2, 1]],
         [[2, 1], [2, 0]],

         [[5, 0], [5, 3]],
         [[5, 3], [4, 3]],
         [[4, 3], [4, 4]],
         [[4, 4], [5, 4]],
         [[5, 4], [5, 5]],
         [[5, 5], [4, 5]],

         [[0, 4], [1, 4]],
         [[1, 4], [1, 5]],
         [[1, 5], [3, 5]],
         [[3, 5], [3, 4]],
         [[2, 5], [2, 3]],

         [[1, 2], [4, 2]],
         [[4, 2], [4, 1]],
         [[4, 1], [3, 1]],
         [[3, 1], [3, 3]],
         [[3, 3], [1, 3]],
         [[1, 3], [1, 2]]]

camera = [0.5, 0.5, 1.5707963]

ray_array = []

fov = 100
screen = [5, 800, 450]


def window_resize(event):
    if (event.keysym == "plus") and (screen[0] < 11):
        screen[0] += 1
    elif (event.keysym == "minus") and (screen[0] > 1):
        screen[0] -= 1
    screen[1] = 160 * screen[0]
    screen[2] = 90 * screen[0]
    canvas.config(width=screen[1], height=screen[2])
    play()


# функция расчёта вероятности столкновения при следующем движении камеры
def collision(displacement):  # true - будет столкновение, false - не будет
    is_collision = False
    for w in range(len(walls)):
        massive = [[cos(displacement[1]), walls[w][0][0] - walls[w][1][0]],
                   [sin(displacement[1]), walls[w][0][1] - walls[w][1][1]]]
        vector_k = [walls[w][0][0] - camera[0], walls[w][0][1] - camera[1]]

        det = massive[0][0] * massive[1][1] - massive[0][1] * massive[1][0]
        if det == 0:
            print("Определитель равен 0")
        inv_matrix = [[massive[1][1] / det, (-1) * massive[0][1] / det],
                      [(-1) * massive[1][0] / det, massive[0][0] / det]]

        vector_u = [inv_matrix[0][0] * vector_k[0] + inv_matrix[0][1] * vector_k[1],   # distance
                    inv_matrix[1][0] * vector_k[0] + inv_matrix[1][1] * vector_k[1]]   # lambda

        if (0 <= vector_u[1] <= 1) and (0 < vector_u[0] <= 1.1 * displacement[0]):
            is_collision = True

    return is_collision


# функция вычисления вектора перемещения и самого движения камеры
def moving(event, speed=0.1, rotation=0.16):
    if event.keysym == 'Left':
        camera[2] += rotation
    elif event.keysym == 'Right':
        camera[2] -= rotation
    else:
        displacement = []
        if event.keycode == 87:  # W
            displacement = [speed, camera[2]]
        elif event.keycode == 65:  # A
            displacement = [speed, camera[2] + 1.5707963]
        elif event.keycode == 83:  # S
            displacement = [speed, camera[2] + 2 * 1.5707963]
        elif event.keycode == 68:  # D
            displacement = [speed, camera[2] + 3 * 1.5707963]

        if displacement:
            if not collision(displacement):
                camera[0] += displacement[0] * cos(displacement[1])
                camera[1] += displacement[0] * sin(displacement[1])

    play()


# функция вычисления длины луча до ближайшей стены
def distance_calculating(i_ray):
    distance = 100
    for w in range(len(walls)):
        massive = [[cos(camera[2] - (i_ray / 100)), walls[w][0][0] - walls[w][1][0]],
                   [sin(camera[2] - (i_ray / 100)), walls[w][0][1] - walls[w][1][1]]]
        vector_k = [walls[w][0][0] - camera[0], walls[w][0][1] - camera[1]]

        det = massive[0][0] * massive[1][1] - massive[0][1] * massive[1][0]
        if det == 0:
            print("Определитель равен 0")
        inv_matrix = [[massive[1][1] / det, (-1) * massive[0][1] / det],
                      [(-1) * massive[1][0] / det, massive[0][0] / det]]

        vector_u = [inv_matrix[0][0] * vector_k[0] + inv_matrix[0][1] * vector_k[1],   # distance
                    inv_matrix[1][0] * vector_k[0] + inv_matrix[1][1] * vector_k[1]]   # lambda

        if (0 <= vector_u[1] <= 1) and (vector_u[0] > 0) and (vector_u[0] < distance):
            distance = vector_u[0]
    return distance


# функция создания массива с расстояниями всех лучей
def raytracing():
    global ray_array
    ray_array.clear()

    for i_ray in range(-80, 81):   # угол обзора -0.8 .. 0.8 рад с шагом 0.01 (161 итерация)
        ray_array.append(distance_calculating(i_ray))


# функция построения всего этого на холсте
def rendering():
    canvas.delete("all")
    center_axis = round(screen[2] / 2)

    for i in range(len(ray_array)):
        color = f'{max((min(round(180 / ray_array[i]), 180)), 18):0>2x}'
        half_wall_height = round((screen[2] * 0.8) / (ray_array[i] * cos(-0.8 + i * 0.01)))
        canvas.create_line((i*screen[0], center_axis - half_wall_height),
                           (i*screen[0], center_axis + half_wall_height),
                           width=screen[0], fill='#'+color*3)

# ((screen[2] * 1) / (ray_array[i] - (ray_array[80] / cos(-0.8 + i * 0.01) - ray_array[80])))


# функция пересчёта данных и перестроения
def play():
    raytracing()
    rendering()


# coded by QWertyIX
if __name__ == '__main__':
    root = tk.Tk()
    root.title("GOTY 2021")

    root.bind("<plus>", window_resize)
    root.bind("<minus>", window_resize)

    root.bind("<Key>", moving)

    canvas = tk.Canvas(master=root, width=800, height=450, relief=tk.FLAT, bg="black", borderwidth=0)
    canvas.pack(expand=1, fill=tk.BOTH)

    # while True:
    #     play()
    #     time.sleep(1 - time.time() % 1)

    play()

    root.mainloop()
