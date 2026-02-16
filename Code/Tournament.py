import random
import numpy as np

TOURNAMENT_SIZE = 2

def run_tournament(population, fitnesses):
    randomIndxs = [] # holds tournament participants

    for j in range(TOURNAMENT_SIZE): # get participants
        randomIndxs.append(np.random.randint(0, len(population) - 1))

    fitnessForParticipants = [] # get participants fitnesses

    for j in range(TOURNAMENT_SIZE):
        fitnessForParticipants.append(fitnesses[randomIndxs[j]])

    # get winner of tournament
    winner = evaluate_round(fitnessForParticipants)

    return population[randomIndxs[winner]] #return winner


def evaluate_round(participants):
    chanceFactor = random.random() # this adds fuzziness to the tournament

    if chanceFactor < 0.6:
        return np.argmax(participants) # there is a 60% chance that the best participant will win
    else:
        return random.randint(0,TOURNAMENT_SIZE-1) # otherwise return a random participant as the winner
