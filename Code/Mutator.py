import copy
import random


def mutate(solution,slotCount,examCount):
    newSolution = copy.deepcopy(solution)
    slot = random.randint(0,slotCount-1)
    slotToChange = newSolution[slot]

    chanceForMod = random.random()
    if chanceForMod < 0.6:
        exam = -1
        if len(slotToChange) > 1:
            exam = random.randint(0,len(slotToChange)-1)

        elif len(slotToChange) == 1:
            exam = 0

        if exam == -1:
            newSolution[slot].append(random.randint(0,examCount-1))

        newSolution[slot][exam] = random.randint(0,examCount-1)
    elif 0.8 > chanceForMod > 0.6:
        slotToChange.append(random.randint(0,examCount-1))
        newSolution[slot] = slotToChange
    else:
        if len(slotToChange) > 0:
            slotToChange.pop()
            newSolution[slot] = slotToChange


    return newSolution

