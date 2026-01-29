import math

import numpy as np

import Setup
import Fitness

if __name__ == '__main__':
    print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("input.txt")

    population = Setup.intialize_population(100, numExams, numSlots)

    fitnesses = []
    for pop in population:
        fitnesses.append(Fitness.evaluate_fitness(pop, numExams,enrollment))

    print(fitnesses)
    fitnesses = np.array(fitnesses)
    five_percent = int(math.floor(len(fitnesses)/20))
    print(five_percent)

    ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]
    print(ind)
    topFivePercent = fitnesses[ind]
    print(topFivePercent)
