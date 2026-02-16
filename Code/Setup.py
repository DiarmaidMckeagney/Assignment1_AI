import random

def generate_random_solution(numExams, numSlots):
    solution = [] # stores solution

    for _ in range(numSlots): # creates the number of slots needed
        slot = []
        slotLength = numExams // numSlots # get the number of values to fill the slot with

        for _ in range(slotLength): # fill slot with random exams
            module = random.randint(0, numExams - 1)
            slot.append(module)

        solution.append(slot)

    return solution


def read_instance(fileName):
    print("Reading input file")
    #open file and read in the lines
    file = open(fileName, 'r')
    enrollment = file.readlines()
    file.close()

    # gets the first line with the numExams, numSlots, and numStudents and splits them into respective vars
    nums = enrollment[0].strip().split(" ")

    numExams = int(nums[0])
    numSlots = int(nums[1])
    numStudents = int(nums[2])

    enrollment.pop(0) # remove first line as it is no longer needed

    # rest of file is the student enrollment matrix
    for i in range(len(enrollment)): # maps the matrix to a list of values
        enrollment[i] = list(map(int, enrollment[i].strip().split()))

    return numExams, numSlots, numStudents, enrollment


def initialize_population(popSize, numExams, numSlots):
    print("Setting up population")
    population = []

    for _ in range(popSize):#generate the population
        population.append(generate_random_solution(numExams, numSlots))
    return population
