import copy
import random
import numpy as np

SWAPPING_CHANCE = 0.8
BALANCE_CHANCE = 0.3
ORIGINAL_MUTATION_CHANCE = 0.6


def mutate(solution,slotCount,examCount, fitness):
    newSolution = copy.deepcopy(solution)

    if fitness >= -243000: # this is a special case for when the pops have 4 or fewer clashes remaining

        slot1 = random.randint(0, slotCount - 1) # get two random slots
        slot2 = random.randint(0, slotCount - 1)

        if newSolution[slot1] and newSolution[slot2]: # if they both exist
            # Swap one exam between slots
            exam1 = random.choice(newSolution[slot1])
            newSolution[slot1].remove(exam1)
            newSolution[slot2].append(exam1)
        return newSolution

    # 80% chance of swapping exams between slots
    if random.random() < SWAPPING_CHANCE:
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
    if max(slot_sizes) > min(slot_sizes) + 1 and random.random() < BALANCE_CHANCE:
        large_slot = np.argmax(slot_sizes)
        small_slot = np.argmin(slot_sizes)
        exam = random.choice(newSolution[large_slot])
        newSolution[large_slot].remove(exam)
        newSolution[small_slot].append(exam)
        return newSolution

    slot = random.randint(0,slotCount-1)
    slotToChange = newSolution[slot]

    if random.random() < ORIGINAL_MUTATION_CHANCE: # chance to pick a slot and change value/add/remove value
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

