import copy
import math
import random
import numpy as np
import Mutator
import Setup
import Crossover, Fitness
from Tournament import run_tournament

GENERATIONS = 2000
POPULATION_SIZE = 170
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.40
DIP_MUTATION_RATE = 0.90
SWAP_RATE = 0.05 # used for diploid swapping
STAGNANT_ROUNDS_COUNTER_MAX = 15
MAX_AMOUNT_OF_STAGNANT_GENS = 40


if __name__ == '__main__':
    #print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("../InputFiles/medium_instance.txt")

    population = Setup.intialize_population(POPULATION_SIZE, numExams, numSlots)
    dipPopulation = Setup.intialize_population(POPULATION_SIZE, numExams, numSlots)

    bestFitness = -1e20
    stagnantGenerations = 0
    isStagnant = False
    stagnantRounds = 0

    maxFitness = []
    for i in range (0, GENERATIONS):
        if stagnantRounds == STAGNANT_ROUNDS_COUNTER_MAX: # resets the mutation rate after a stagnation change
            MUTATION_RATE = 0.2
            CROSSOVER_RATE = 0.5
            isStagnant = False
            Mutator.SWAPPING_CHANCE = 0.8
            Mutator.BALANCE_CHANCE = 0.3
            Mutator.ORIGINAL_MUTATION_CHANCE = 0.6
        elif isStagnant: # the stagnation changes should stay for STAGNANT_ROUNDS_COUNTER_MAX rounds
            stagnantRounds += 1

        fitnesses = []

        for pop in population:
            fitnesses.append(Fitness.evaluate_fitness(pop, numExams, enrollment))

        if fitnesses.count(0) > 0:
            print(f'finished on gen {i}')
            break
        fitnesses = np.array(fitnesses)
        #print(fitnesses)

        # Track global best fitness
        if len(maxFitness) > 20:
            if maxFitness[i-1] <= maxFitness[i-20]:
                stagnantGenerations += 1
            else:
                stagnantGenerations = max(0, stagnantGenerations - 1)

        nextGeneration = []

           # Check for stagnation
        if stagnantGenerations >= MAX_AMOUNT_OF_STAGNANT_GENS:
            isStagnant = True
            MUTATION_RATE = 0.9
            CROSSOVER_RATE = 0.2
            Mutator.SWAPPING_CHANCE = 1
            Mutator.BALANCE_CHANCE = 1
            Mutator.ORIGINAL_MUTATION_CHANCE = 0
            stagnantRounds += 1

            print(f"Stagnation detected at generation {i}. Fitness: {max(fitnesses)}")

            # If stagnated, inject new random solutions for diversity
            while len(nextGeneration) < POPULATION_SIZE * 0.35:
                nextGeneration.append(Setup.generate_random_solution(numExams, numSlots))

            stagnantGenerations = 0

        # Elite selection - keep the top 5% of the population for the next generation
        five_percent = int(math.floor(len(fitnesses) / 20))
        ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]

        topFivePercent = fitnesses[ind]
        for pop in ind:
            nextGeneration.append(copy.deepcopy(population[pop]))

        # Fill the rest of the next generation using tournament selection, crossover and mutation
        while len(nextGeneration) < POPULATION_SIZE:
            parent1 = run_tournament(population, fitnesses)

            if random.random() < CROSSOVER_RATE:
                parent2 = run_tournament(population, fitnesses)
                child1, child2 = Crossover.crossover(parent1, parent2, numSlots)

                # Mutation
                if random.random() < MUTATION_RATE:
                    child1Fitness = Fitness.evaluate_fitness(child1, numExams, enrollment)
                    child1 = Mutator.mutate(child1,numSlots, numExams, child1Fitness)
                if random.random() < MUTATION_RATE:
                    child2Fitness = Fitness.evaluate_fitness(child2, numExams, enrollment)
                    child2 = Mutator.mutate(child2, numSlots, numExams, child2Fitness)

                nextGeneration.append(child1)
                if len(nextGeneration) < POPULATION_SIZE:
                    nextGeneration.append(child2)
            else:
                # Clone and mutate
                child = copy.deepcopy(parent1)
                if random.random() < MUTATION_RATE:
                    childFitness = Fitness.evaluate_fitness(child, numExams, enrollment)
                    child = Mutator.mutate(child, numSlots, numExams,childFitness)
                nextGeneration.append(child)

        for i in range(len(dipPopulation)):
            if random.random() < DIP_MUTATION_RATE:
                dipFitness = Fitness.evaluate_fitness(dipPopulation[i],numExams, enrollment)
                dipPopulation[i] = Mutator.mutate(dipPopulation[i], numSlots, numExams,dipFitness)

        crossoverCounter = 0
        while crossoverCounter < POPULATION_SIZE:
            if random.random() < CROSSOVER_RATE:
                dipPopulation[crossoverCounter], dipPopulation[crossoverCounter +1] = Crossover.crossover(dipPopulation[crossoverCounter],dipPopulation[crossoverCounter +1],numSlots)
            crossoverCounter += 2

        for i in range(len(nextGeneration)):
            if random.random() < SWAP_RATE:
                dipValue = copy.deepcopy(dipPopulation[i])
                nextGenValue = copy.deepcopy(nextGeneration[i])
                dipPopulation[i] = nextGenValue
                nextGeneration[i] = dipValue

        maxFit = np.max(fitnesses)
        maxFitness.append(int(maxFit))
        population.clear()
        population = nextGeneration

    finalFitness = []
    finalFitnessDip = []
    for i in range(len(population)):
        finalFitness.append(Fitness.evaluate_fitness(population[i], numExams, enrollment))
        finalFitnessDip.append(Fitness.evaluate_fitness(dipPopulation[i], numExams, enrollment))
    #print("The Final Fitnesses: ", finalFitness)

    finalFitness = np.array(finalFitness)
    finalFitnessDip = np.array(finalFitnessDip)
    #print(finalFitness)

    five_percent = int(math.floor(len(finalFitness) / 20))

    ind = np.argpartition(finalFitness, -five_percent)[-five_percent:]
    indDip = np.argpartition(finalFitnessDip, -five_percent)[-five_percent:]

    topFivePercent = finalFitness[ind]
    topFivePercentDip = finalFitnessDip[indDip]
    print(f'top 5% of last gen: {topFivePercent}')
    print(f'top 5% of last gens Diploid: {topFivePercentDip}')
    print(f'Max Fitness of final gen: {max(finalFitness)}')
    print(f'Max Fitness of last gens Diploid: {max(finalFitnessDip)}')
    print(f'Fitnesses of last gen: {finalFitness}')
    print(f'Fitnesses of last gens diploid: {finalFitnessDip}')
    print("best timetable in last gen: ", population[finalFitness.argmax()], "with fitness: ", finalFitness.max())
    print("best timetable in last gens Diploid: ", dipPopulation[finalFitnessDip.argmax()], "with fitness: ", finalFitnessDip.max())
    print("The max fitnesses of each gen: ",maxFitness)