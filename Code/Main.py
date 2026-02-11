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

    bestFitness = -1e20
    stagnantGenerations = 0


    maxFitness = []
    for i in range (0, GENERATIONS):
        fitnesses = []
        for pop in population:
            fitnesses.append(Fitness.evaluate_fitness(pop, numExams, enrollment))

        fitnesses = np.array(fitnesses)
        #print(fitnesses)

        # Track global best fitness
        if len(maxFitness) > 20:
            if maxFitness[i-1] <= maxFitness[i-20]:
                stagnantGenerations += 1
            else:
                stagnantGenerations = max(0, stagnantGenerations - 1)

        nextGeneration = []

        # Elite selection - keep the top 5% of the population for the next generation
        five_percent = int(math.floor(len(fitnesses)/20))
        ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]

        topFivePercent = fitnesses[ind]
        for pop in ind:
            nextGeneration.append(copy.deepcopy(population[pop]))

           # Check for stagnation
        if stagnantGenerations >= 100:
            print(f"Stagnation detected at generation {i}.")
            # If stagnated, inject new random solutions for diversity
            while len(nextGeneration) < POPULATION_SIZE * 0.35:
                nextGeneration.append(Setup.generate_random_solution(numExams, numSlots))
            stagnantGenerations = 0

        # Fill the rest of the next generation using tournament selection, crossover and mutation
        while len(nextGeneration) < POPULATION_SIZE:
            parent1 = run_tournament(population, fitnesses, i)

            if random.random() < CROSSOVER_RATE:
                parent2 = run_tournament(population, fitnesses, i)
                child1, child2 = Crossover.crossover(parent1, parent2, numSlots)

                # Mutation
                if random.random() < MUTATION_RATE:
                    child1 = Mutator.mutate(child1,numSlots, numExams)
                if random.random() < MUTATION_RATE:
                    child2 = Mutator.mutate(child2, numSlots, numExams)

                nextGeneration.append(child1)
                if len(nextGeneration) < POPULATION_SIZE:
                    nextGeneration.append(child2)
            else:
                # Clone and mutate
                child = copy.deepcopy(parent1)
                if random.random() < MUTATION_RATE:
                    child = Mutator.mutate(child, numSlots, numExams)
                nextGeneration.append(child)



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