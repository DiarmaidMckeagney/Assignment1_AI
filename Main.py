import copy
import math
import random

import numpy as np

import Mutator
import Setup
import Fitness
import Crossover
from Tournament import run_tournament

GENERATIONS = 100
POPULATION_SIZE = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.10
TOURNAMENT_SIZE = 3

if __name__ == '__main__':
    print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("trainingExample2.txt")

    population = Setup.intialize_population(100, numExams, numSlots)

    maxFitness = []
    for i in range (0, GENERATIONS):
        fitnesses = []
        for pop in population:
            fitnesses.append(Fitness.evaluate_fitness(pop, numExams,enrollment))

        fitnesses = np.array(fitnesses)
        print(fitnesses)

        five_percent = int(math.floor(len(fitnesses)/20))

        ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]

        topFivePercent = fitnesses[ind]
        print(f'top 5% of gen {i}: {topFivePercent}')

        nextGeneration = []

        for pop in ind:
            nextGeneration.append(copy.deepcopy(population[pop]))

        print(f'The elite of gen {i}: {nextGeneration}')
        while len(nextGeneration) < POPULATION_SIZE:
            winnerOne = run_tournament(population, fitnesses)

            chanceForCrossover = random.random()

            if chanceForCrossover < CROSSOVER_RATE and len(nextGeneration) < POPULATION_SIZE - 1:
                winnerTwo = run_tournament(population, fitnesses)

                childOne,childTwo = Crossover.crossover(winnerOne, winnerTwo)

                if random.random() < MUTATION_RATE:
                    childOne = Mutator.mutate(childOne,numSlots,numExams)

                if random.random() < MUTATION_RATE:
                    childTwo = Mutator.mutate(childTwo,numSlots,numExams)

                nextGeneration.append(childOne)
                nextGeneration.append(childTwo)

            else:
                if random.random() < MUTATION_RATE:
                    winnerOne = Mutator.mutate(winnerOne,numSlots,numExams)

                nextGeneration.append(winnerOne)
        maxFit = np.max(fitnesses)
        maxFitness.append(int(maxFit))
        population.clear()
        population = nextGeneration

    finalFitness = []
    for i in range(len(population)):
        finalFitness.append(Fitness.evaluate_fitness(population[i],numExams,enrollment))
    print("The Final Fitnesses: ", finalFitness)

    finalFitness = np.array(finalFitness)
    print(finalFitness)

    five_percent = int(math.floor(len(finalFitness) / 20))

    ind = np.argpartition(finalFitness, -five_percent)[-five_percent:]

    topFivePercent = finalFitness[ind]
    print(f'top 5% of last gen: {topFivePercent}')
    print("first timetable in last gen: ", population[0])
    print("The max fitnesses of each gen: ",maxFitness)