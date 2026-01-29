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


def intialize_population():
    print("Setting up population")