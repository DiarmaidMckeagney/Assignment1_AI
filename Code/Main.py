import copy
import math
import random
import numpy as np
import Mutator
import Setup
import Crossover, Fitness
from Tournament import run_tournament

GENERATIONS = 500
POPULATION_SIZE = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.05

if __name__ == '__main__':
    random.seed(2) # set seed for reproducibility

    #print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("InputFiles/small.txt")

    population = Setup.intialize_population(POPULATION_SIZE, numExams, numSlots)

    maxFitness = []
    for i in range (0, GENERATIONS):
        fitnesses = []
        for pop in population:
            fitnesses.append(Fitness.evaluate_fitness(pop, numExams, enrollment))

        fitnesses = np.array(fitnesses)
        #print(fitnesses)

        five_percent = int(math.floor(len(fitnesses)/10))

        ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]

        topFivePercent = fitnesses[ind]
        #print(f'top 5% of gen {i}: {topFivePercent}')

        nextGeneration = []

        for pop in ind:
            nextGeneration.append(copy.deepcopy(population[pop]))

        while len(nextGeneration) < POPULATION_SIZE:
            winnerOne = run_tournament(population, fitnesses)

            chanceForCrossover = random.random()

            if chanceForCrossover < CROSSOVER_RATE and len(nextGeneration) < POPULATION_SIZE - 1:
                winnerTwo = run_tournament(population, fitnesses)

                childOne,childTwo = Crossover.crossover(winnerOne, winnerTwo, numSlots)

                if random.random() < MUTATION_RATE:
                    childOne = Mutator.mutate(childOne, numSlots, numExams)

                if random.random() < MUTATION_RATE:
                    childTwo = Mutator.mutate(childTwo, numSlots, numExams)

                nextGeneration.append(childOne)
                nextGeneration.append(childTwo)

            else:
                if random.random() < MUTATION_RATE:
                    winnerOne = Mutator.mutate(winnerOne, numSlots, numExams)

                nextGeneration.append(winnerOne)
        maxFit = np.max(fitnesses)
        maxFitness.append(int(maxFit))
        population.clear()
        population = nextGeneration

    finalFitness = []
    for i in range(len(population)):
        finalFitness.append(Fitness.evaluate_fitness(population[i], numExams, enrollment))
    #print("The Final Fitnesses: ", finalFitness)

    finalFitness = np.array(finalFitness)
    #print(finalFitness)

    five_percent = int(math.floor(len(finalFitness) / 20))

    ind = np.argpartition(finalFitness, -five_percent)[-five_percent:]

    topFivePercent = finalFitness[ind]
    print(f'top 5% of last gen: {topFivePercent}')
    print("best timetable in last gen: ", population[finalFitness.argmax()], "with fitness: ", finalFitness.max())
    print("The max fitnesses of each gen: ",maxFitness)