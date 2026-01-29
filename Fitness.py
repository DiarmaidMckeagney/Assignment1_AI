


def evaluate_fitness(solution, moduleCount,students):
    hardConstraintScore = 0 # tracks the hard constraints
    softConstraintScore = 0 # tracks the soft constraints

    # this tracks the number of times each module is timetabled
    moduleCountTracker = [0] * (moduleCount + 1)

    # going through each module in each slot and counting the occurrence
    for slot in solution:
        for module in slot:
            moduleCountTracker[module] += 1

    # goes through and punishes duplicate module timetabling
    for i in moduleCountTracker:
        if i == 1:
            hardConstraintScore += 100
        elif i == 0:
            hardConstraintScore -= 100
        else:
            hardConstraintScore -= 100

    #going through each student and checking for clashing exams and punishing them
    for student in students:
        for slot in solution:
            examsInThisSlot = 0
            for module in slot:
                if student[module - 1] == 1:
                    examsInThisSlot += 1

            if examsInThisSlot <= 1:
                hardConstraintScore += 100
            else:
                hardConstraintScore -= 100

    return hardConstraintScore





if __name__ == '__main__':
    solution = [[6,2,5],[4,6,1]]
    moduleCount = 6
    students = [[0,1,1,0,0,1],[1,1,0,0,0,0],[0,1,0,1,0,0]]

    #used to test the fitness function.
    print(evaluate_fitness(solution, moduleCount,students))

