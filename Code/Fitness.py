


def evaluate_fitness(solution, numExams, enrollment):
    hardConstraintScore = 0 # tracks the hard constraints

    #Punishent Hierarchy:
    #Missing exams
    #Invalid exam code
    #Duplicate exams
    #Student clash
    #Slot imblance (prevents all exams being in one slot, this is a soft constraint, helps prevent overloading a slot)
    


    # Check for missing, duplicate or invalid exams
    examCount = [0] * numExams
    for slot in solution:
        for exam in slot:
            if exam < 0 or exam >= numExams:
                return -1e9 # invalid exam code, gets "death penalty"
            if examCount[exam] > 0:
                hardConstraintScore -= 1e5 # duplicate exam -100,000
            examCount[exam] += 1

    for count in examCount:
        if count == 0:
            hardConstraintScore -= 1e12 # missing exam, should be unrecoverable if missing exams

    # Check for student clashes
    for student in enrollment:
        studentExamSlots = {}
        for slotIdx, slotExams in enumerate(solution):
            for exam in slotExams:
                if student[exam] == 1:
                    if slotIdx in studentExamSlots:
                        hardConstraintScore -= 50000 # student clash -50,000
                        #print(f"Student clash detected for student {student} in slot {slotIdx}")
                    else:
                        studentExamSlots[slotIdx] = True
        
        # Check for missing exams for this student
        enrolledCount = sum(student)
        scheduledCount = len(studentExamSlots)
        if enrolledCount > scheduledCount:
            hardConstraintScore -= 10000 # missing exam for student -10,000
            #print(f"Missing exam detected for student {student}. Enrolled in {enrolledCount} exams but only {scheduledCount} scheduled.")

    # Check for slot imbalance (soft constraint)
    slotSizes = [len(slot) for slot in solution]
    imbalance = max(slotSizes) - min(slotSizes)
    hardConstraintScore -= imbalance * 1000  # Push toward even distribution

    #Punish solutions that have slots with over the average exams per slot
    averageExamsPerSlot = numExams / len(solution)
    for slot in solution:
        if len(slot) > averageExamsPerSlot:
            hardConstraintScore -= (len(slot) - averageExamsPerSlot) * 1000


    #print(f"numexams: {numExams}, solution size: {len(solution)}, enrollment size: {len(enrollment)}")

    return hardConstraintScore


if __name__ == '__main__':
    solution = [[0, 2], [1], [3]]
    moduleCount = 4
    students = [[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,1,0,1]]

    #used to test the fitness function.
    print("Testing fitness function with solution: ", solution)
    print(evaluate_fitness(solution, moduleCount,students))

