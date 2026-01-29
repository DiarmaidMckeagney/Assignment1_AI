


def evaluate_fitness(solution, moduleCount,students):
    hardConstraintScore = 0
    softConstraintScore = 0

    moduleCountTracker = [0] * (moduleCount + 1)
    for slot in solution:
        for module in slot:
            moduleCountTracker[module] += 1
    print(moduleCountTracker)
    for i in moduleCountTracker:
        if i == 1:
            hardConstraintScore += 100
        else:
            hardConstraintScore -= 100

    for student in students:
        for slot in solution:
            examsInThisSlot = 0
            for module in slot:
                if student[module - 1] == 1:
                    examsInThisSlot += 1
            print(f"examsInThisSlot {examsInThisSlot} for student {student}")
            if examsInThisSlot <= 1:
                hardConstraintScore += 100
            else:
                hardConstraintScore -= 100

    return hardConstraintScore





if __name__ == '__main__':
    solution = [[6,2,5],[4,6,1]]
    moduleCount = 6
    students = [[0,1,1,0,0,1],[1,1,0,0,0,0],[0,1,0,1,0,0]]
    print(evaluate_fitness(solution, moduleCount,students))

