import copy
import random
import numpy as np


def mutate(solution,slotCount,examCount):
    newSolution = copy.deepcopy(solution)

    # 50% chance of swapping exams between slots
    if random.random() < 0.5:
        slot1, slot2 = random.sample(range(slotCount), 2)
        if newSolution[slot1] and newSolution[slot2]:
            # Swap one exam between slots
            exam1 = random.choice(newSolution[slot1])
            exam2 = random.choice(newSolution[slot2])
            newSolution[slot1].remove(exam1)
            newSolution[slot2].remove(exam2)
            newSolution[slot1].append(exam2)
            newSolution[slot2].append(exam1)
            return newSolution
    
    # 30% chance to move an exam from a larger slot to a smaller slot to reduce imbalance
    slot_sizes = [len(s) for s in newSolution]
    if max(slot_sizes) > min(slot_sizes) + 1 and random.random() < 0.3:
        large_slot = np.argmax(slot_sizes)
        small_slot = np.argmin(slot_sizes)
        exam = random.choice(newSolution[large_slot])
        newSolution[large_slot].remove(exam)
        newSolution[small_slot].append(exam)
        return newSolution

    slot = random.randint(0,slotCount-1)
    slotToChange = newSolution[slot]

    if random.random() < 0.6:
        exam = -1
        if len(slotToChange) > 1:
            exam = random.randint(0,len(slotToChange)-1)

        elif len(slotToChange) == 1:
            exam = 0

        if exam == -1:
            newSolution[slot].append(random.randint(0,examCount-1))

        newSolution[slot][exam] = random.randint(0,examCount-1)
    elif len(slotToChange) < 4:
        slotToChange.append(random.randint(0,examCount-1))
        newSolution[slot] = slotToChange
    else:
        if len(slotToChange) > 0:
            slotToChange.pop()
            newSolution[slot] = slotToChange


    return newSolution

