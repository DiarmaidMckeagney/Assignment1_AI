import Setup
import Fitness

if __name__ == '__main__':
    print("hello world")
    numExams, numSlots, numStudents, enrollment = Setup.read_instance("input.txt")

    population = Setup.intialize_population(2, numExams, numSlots)
