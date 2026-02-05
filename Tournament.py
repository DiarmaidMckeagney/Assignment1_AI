import numpy as np

TOURNAMENT_SIZE = 4
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
    return np.argmax(participants)
