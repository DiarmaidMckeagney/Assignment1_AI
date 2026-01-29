import random


def mutate(solution,moduleCount):
    slot = random.randint(0,moduleCount)
    slotToChange = solution[slot]
    exam = random.randint(0,len(slotToChange)-1)

    solution[slot][exam] = random.randint(0,moduleCount)

