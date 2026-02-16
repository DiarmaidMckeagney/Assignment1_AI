import random


def crossover(parent1, parent2,slotCount):
    #get number of times to crossover
    numIter = random.randint(1,2)
    child1, child2 = [],[]

    for i in range(numIter):
        #get random point to crossover at
        splitIndex = random.randint(1,slotCount -1)

        #crossover
        child1 = parent1[:splitIndex] + parent2[splitIndex:]
        child2 = parent2[:splitIndex] + parent1[splitIndex:]

    return child1, child2