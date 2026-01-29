import Setup

if __name__ == '__main__':
    print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("input.txt")

    print("Number of Exams:", numExams)
    print("Number of Slots:", numSlots)
    print("Number of Students:", numStudents)
    print("Enrollment Data:", enrollment)
