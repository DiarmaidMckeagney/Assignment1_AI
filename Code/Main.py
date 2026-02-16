import copy
import math
import random
import numpy as np
import Mutator
import Setup
import Crossover, Fitness
from Tournament import run_tournament
import matplotlib as plt


GENERATIONS = 2500
POPULATION_SIZE = 170

CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.40

DIP_MUTATION_RATE = 0.90 # the diploid group will have a much higher mutation rate than the main population
SWAP_RATE = 0.05 # Rate of swapping between diploid group and main population

STAGNANT_ROUNDS_COUNTER_MAX = 15 # The number of generations subject to hypermutation after a stagnation has been found to occur
MAX_AMOUNT_OF_STAGNANT_GENS = 40 # The number of rounds the max fitness need to stay the same for it to count as stagnation.


if __name__ == '__main__':
    #read in Input File
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("../InputFiles/small.txt")# NOTE: needs ../ for linux but nothing for windows

    #setup randomly generated population and diploid population
    population = Setup.initialize_population(POPULATION_SIZE, numExams, numSlots)
    dipPopulation = Setup.initialize_population(POPULATION_SIZE, numExams, numSlots)

    bestFitness = -1e20 #set so low as the initial fitnesses are likely to be very low.
    stagnantGenerations = 0 # tracks how many rounds have the same max fitness
    isStagnant = False # used to reset the mutation and crossover rates when hypermutation ends
    hyperMutateRounds = 0 # counter to track how many rounds of hypermutation has occured

    maxFitness = [] # tracks the max fitness of each generation
    for i in range (0, GENERATIONS):
        if hyperMutateRounds == STAGNANT_ROUNDS_COUNTER_MAX: # resets the mutation rate after a stagnation change
            MUTATION_RATE = 0.4
            CROSSOVER_RATE = 0.5
            isStagnant = False
            Mutator.SWAPPING_CHANCE = 0.8
            Mutator.BALANCE_CHANCE = 0.3
            Mutator.ORIGINAL_MUTATION_CHANCE = 0.6
        elif isStagnant: # the stagnation changes should stay for STAGNANT_ROUNDS_COUNTER_MAX rounds
            hyperMutateRounds += 1

        fitnesses = [] # tracks fitness of each pop in population
        dipFitnesses = [] # tracks fitness of each pop in diploid population

        # obtain fitnesses
        for pop in population:
            fitnesses.append(Fitness.evaluate_fitness(pop, numExams, enrollment))

        for dipPop in dipPopulation:
            dipFitnesses.append(Fitness.evaluate_fitness(dipPop,numExams, enrollment))

        # Ends search if optimal solution is found.
        if fitnesses.count(0) > 0 or dipFitnesses.count(0) > 0:
            print(f'finished on gen {i}')
            break

        fitnesses = np.array(fitnesses) # converted to a numpy array for easier processing


        # Track global best fitness
        if len(maxFitness) > 20: # only starts after 20 generations.
            if maxFitness[i-1] <= maxFitness[i-20]:
                stagnantGenerations += 1
            else:
                stagnantGenerations = max(0, stagnantGenerations - 1)

        nextGeneration = []

           # Check for stagnation
        if stagnantGenerations >= MAX_AMOUNT_OF_STAGNANT_GENS:
            isStagnant = True
            MUTATION_RATE = 0.9 #up the mutation rate
            CROSSOVER_RATE = 0.2 # lower the crossover rate
            Mutator.SWAPPING_CHANCE = 1 # make the chance that a
            Mutator.BALANCE_CHANCE = 1
            Mutator.ORIGINAL_MUTATION_CHANCE = 0
            hyperMutateRounds += 1

            print(f"Stagnation detected at generation {i}. Fitness: {max(fitnesses)}")

            # If stagnated, inject new random solutions for diversity
            while len(nextGeneration) < POPULATION_SIZE * 0.35:
                nextGeneration.append(Setup.generate_random_solution(numExams, numSlots))

            stagnantGenerations = 0

        # Elite selection - keep the top 5% of the population for the next generation
        five_percent = int(math.floor(len(fitnesses) / 20))

        # gets the indexes of the top five percent
        ind = np.argpartition(fitnesses, -five_percent)[-five_percent:]

        # gets the values of the top five percent
        topFivePercent = fitnesses[ind]

        # append to next gen
        for pop in ind:
            nextGeneration.append(copy.deepcopy(population[pop]))

        # Fill the rest of the next generation using tournament selection, crossover and mutation
        while len(nextGeneration) < POPULATION_SIZE:
            #run initial tournament and get the winner
            parent1 = run_tournament(population, fitnesses)

            if random.random() < CROSSOVER_RATE:
                # if crossover, run second tournament to get the second parent
                parent2 = run_tournament(population, fitnesses)
                #crossover to get child1 and child2
                child1, child2 = Crossover.crossover(parent1, parent2, numSlots)

                # Mutation
                if random.random() < MUTATION_RATE: # individual chance of each child getting a mutation
                    child1Score = Fitness.evaluate_fitness(child1, numExams, enrollment) # evaluating child to pass score into mutation function
                    child1 = Mutator.mutate(child1, numSlots, numExams, child1Score) # mutate child
                if random.random() < MUTATION_RATE:
                    child2Score = Fitness.evaluate_fitness(child2, numExams, enrollment)
                    child2 = Mutator.mutate(child2, numSlots, numExams, child2Score)

                nextGeneration.append(child1)
                if len(nextGeneration) < POPULATION_SIZE: # this ensures our population doesn't get larger
                    nextGeneration.append(child2)
            else: # case of no crossover
                # Clone and mutate
                child = copy.deepcopy(parent1)

                if random.random() < MUTATION_RATE:
                    childFitness = Fitness.evaluate_fitness(child, numExams, enrollment)
                    child = Mutator.mutate(child, numSlots, numExams,childFitness)

                nextGeneration.append(child)

        for i in range(len(dipPopulation)): # mutate the diploid population
            if random.random() < DIP_MUTATION_RATE:
                dipFitness = Fitness.evaluate_fitness(dipPopulation[i],numExams, enrollment)
                dipPopulation[i] = Mutator.mutate(dipPopulation[i], numSlots, numExams,dipFitness)

        crossoverCounter = 0 # counts the number of pops that have been (maybe) crossed
        while crossoverCounter < POPULATION_SIZE: # crossover for diploid population
            if random.random() < CROSSOVER_RATE:
                dipPopulation[crossoverCounter], dipPopulation[crossoverCounter +1] = Crossover.crossover(dipPopulation[crossoverCounter],dipPopulation[crossoverCounter +1],numSlots)
            crossoverCounter += 2

        for i in range(len(nextGeneration)): # swapping in diploid pops into the main pop and vice versa
            if random.random() < SWAP_RATE:
                dipValue = copy.deepcopy(dipPopulation[i])
                nextGenValue = copy.deepcopy(nextGeneration[i])
                dipPopulation[i] = nextGenValue
                nextGeneration[i] = dipValue

        maxFit = np.max(fitnesses) # getting max fitness of population
        maxFitness.append(int(maxFit))

        population.clear() # clearing pop list to avoid issues
        population = nextGeneration # setting pop to the next generation

    ## FINISHED SEARCH
    finalFitness = [] # getting final fitnesses of pop and diploid pop
    finalFitnessDip = []

    for i in range(len(population)): # evaluating fitnesses
        finalFitness.append(Fitness.evaluate_fitness(population[i], numExams, enrollment))
        finalFitnessDip.append(Fitness.evaluate_fitness(dipPopulation[i], numExams, enrollment))


    finalFitness = np.array(finalFitness) # setting them as numpy arrays for easier processing
    finalFitnessDip = np.array(finalFitnessDip)


    five_percent = int(math.floor(len(finalFitness) / 20))

    ind = np.argpartition(finalFitness, -five_percent)[-five_percent:] # getting final top five percent
    indDip = np.argpartition(finalFitnessDip, -five_percent)[-five_percent:]

    topFivePercent = finalFitness[ind]
    topFivePercentDip = finalFitnessDip[indDip]

    #printing info
    print(f'top 5% of last gen: {topFivePercent}')
    print(f'top 5% of last gens Diploid: {topFivePercentDip}')
    print(f'Max Fitness of final gen: {max(finalFitness)}')
    print(f'Max Fitness of last gens Diploid: {max(finalFitnessDip)}')
    print(f'Fitnesses of last gen: {finalFitness}')
    print(f'Fitnesses of last gens diploid: {finalFitnessDip}')
    print("best timetable in last gen: ", population[finalFitness.argmax()], "with fitness: ", finalFitness.max())
    print("best timetable in last gens Diploid: ", dipPopulation[finalFitnessDip.argmax()], "with fitness: ", finalFitnessDip.max())
    print("The max fitnesses of each gen: ",maxFitness)