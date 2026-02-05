import random

import numpy as np

TOURNAMENT_SIZE = 3
def run_tournament(population, fitnesses):
    randomIndxs = []

    for j in range(TOURNAMENT_SIZE):
        randomIndxs.append(np.random.randint(0, len(population) - 1))

    fitnessForParticipants = []

    for j in range(TOURNAMENT_SIZE):
        fitnessForParticipants.append(fitnesses[randomIndxs[j]])

    winner = evaluate_round(fitnessForParticipants)

    return population[randomIndxs[winner]]


def evaluate_round(participants):
    chanceFactor = random.random()

    if chanceFactor < 0.5:
        return np.argmax(participants)
    else:
        return random.randint(0,TOURNAMENT_SIZE-1)
