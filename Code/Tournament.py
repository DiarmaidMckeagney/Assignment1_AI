import random

import numpy as np

TOURNAMENT_SIZE = 3
def run_tournament(population, fitnesses, generation):
    tournamentSize = max(2, 7-generation//75)
    randomIndxs = []

    for j in range(tournamentSize):
        randomIndxs.append(np.random.randint(0, len(population) - 1))

    fitnessForParticipants = []

    for j in range(tournamentSize):
        fitnessForParticipants.append(fitnesses[randomIndxs[j]])

    winner = evaluate_round(fitnessForParticipants, tournamentSize)

    return population[randomIndxs[winner]]


def evaluate_round(participants, tournamentSize):
    chanceFactor = random.random()

    if chanceFactor < 0.5:
        return np.argmax(participants)
    else:
        return random.randint(0,tournamentSize-1)
