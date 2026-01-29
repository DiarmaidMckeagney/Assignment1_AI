import random

def read_instance(fileName):
    print("Reading input file")
    
    file = open(fileName, 'r')
    enrollment = file.readlines()
    file.close()

    numExams = int(enrollment[0][0])
    numSlots = int(enrollment[0][2])
    numStudents = int(enrollment[0][4])
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
                module = random.randint(1, numExams)
                slot.append(module)
            solution.append(slot)
        population.append(solution)

    return population
