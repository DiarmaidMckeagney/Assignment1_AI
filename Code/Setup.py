import random

def read_instance(fileName):
    print("Reading input file")
    
    file = open(fileName, 'r')
    enrollment = file.readlines()
    file.close()

    nums = enrollment[0].strip().split()
    numExams = int(nums[0])
    numSlots = int(nums[1])
    numStudents = int(nums[2])
    enrollment.pop(0)

    for i in range(len(enrollment)):
        enrollment[i] = list(map(int, enrollment[i].strip().split()))

    return numExams, numSlots, numStudents, enrollment


def intialize_population(popSize, numExams, numSlots):
    print("Setting up population")
    population = []

    for i in range(popSize):
        solution = []
        for j in range(numSlots):
            slot = []
            slotLength = random.randint(0, numExams)
            for k in range(slotLength):
                module = random.randint(0, numExams - 1)
                slot.append(module)
            solution.append(slot)
        population.append(solution)

    return population
