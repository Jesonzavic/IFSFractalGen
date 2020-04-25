import numpy as np
import matplotlib.pyplot as plt
import random
from math import *

class IFS():
    # Class that holds the important elements of an IFS matrix 
    # transformation, the multiplier and translation

    ## defult initiator input:
    # ifs = IFS(([x-horizon, y-horizon],
    #            [x-verticl, y-verticl])#, [x-translation, y-translation]) #translation is optional

    translation = np.array(([0],[0]))
    def __init__(self, multiplier,translation=None):
        self.multiplier = np.array(multiplier)
        if translation:
            self.translation = translation
    def set_translation(self, translation):
        self.translation = np.array(translation)

def apply_transformation(xy, function):
    # Applies the IFS multiplier and translation of the function given
    # to a point, and then returns that shifted point

    xy = np.dot(function.multiplier, xy)
    xy = np.add(xy, function.translation)
    return xy

def calculate_functions_area(functions):
    #takes a list of IFS functions and returns the total area of the shapes they make

    total_area = 0
    for func in functions:
        total_area += np.linalg.det(func.multiplier)
    return total_area

def calculate_func_area_ratios(functions, total_area):
    # calculates the ratio of area to total area from the shape the functions create

    function_ratios = []
    for func in functions:
        function_ratios.append(np.linalg.det(func.multiplier)/total_area)
    return function_ratios

def choose_random_weighted_element(functions, weightings):
    ### Chooses a random element of functions, weighted by the weightings list

    i = 0
    random_number = random.randint(1, 10001)
    cur_ratios = [int(i*1000) for i in weightings]
    current_held_number = cur_ratios[0]

    while True:
        if i >= len(functions):
            return choose_random_weighted_element(functions, weightings)
        
        if random_number <= current_held_number:
            return functions[i]
        i += 1
        current_held_number += cur_ratios[1]

def create_plot(x_vals, y_vals):
    plt.title("Visialisation of fractal using Chaos Game and IFS")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x_vals, y_vals, 'bo', label='Fractal Points', markersize=1)
    plt.legend(loc='upper right')

### Example functions for right angled sierpinski triangle
functions = [
            IFS(([.5, 0],
                 [0, .5]),  ([0],  [.5])),
            IFS(([.5, 0],
                 [0, .5]),  ([0],  [0])),
            IFS(([.5, 0],
                 [0, .5]),  ([.5], [0]))
            ]

number_points = 10000

xy = np.array(([.5],[.5]))
points = []

area_ratios = calculate_func_area_ratios(functions, calculate_functions_area(functions))

for i in range(number_points):
    xy = apply_transformation(xy, choose_random_weighted_element(functions, area_ratios))
    points.append(xy)

create_plot([i[0] for i in points], [i[1] for i in points])

#### Save the plot figure to current directory
# plt.savefig('filename.png', dpi=300)

plt.show()