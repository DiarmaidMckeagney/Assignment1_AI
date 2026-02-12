import random


def crossover(parent1, parent2,slotCount):
    numIter = random.randint(1,2)
    child1, child2 = [],[]
    for i in range(numIter):
        splitIndex = random.randint(1,slotCount -1)
        child1 = parent1[:splitIndex] + parent2[splitIndex:]
        child2 = parent2[:splitIndex] + parent1[splitIndex:]

    return child1, child2