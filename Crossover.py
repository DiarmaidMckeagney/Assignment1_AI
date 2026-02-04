def crossover(parent1, parent2):
    crossPoint = len(parent1) // 2
    child1 = parent1[:crossPoint] + parent2[crossPoint:]
    child2 = parent2[:crossPoint] + parent1[crossPoint:]

    return child1, child2