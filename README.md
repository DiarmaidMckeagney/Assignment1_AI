# Assignment 1 for Artificial Intelligence

Peter Fitzgerald - 22323303 <br>
Diarmaid McKeagney - 22321376

This is an assignment to attempt to find a solution to a timetabling problem. We have a set of students with exams, and we need to generate a timetable that doesn't have any clashes in it.

## Code Structure
All code is stored in the Code Directory. The input files are stored in the InputFiles directory. The results from our experiments are stored in the Experiment Results Directory.

The Main.py file is central file in the script. The Setup.py is in charge of reading in the input files and 
creating the initial populations. The Fitness.py script evaluates the fitness of a given pop. The Tournament.py runs the tournament selection for a given population.
The Mutator.py mutates a given solution into a new solution. Crossover.py crosses two solutions at a random point a number of times.

## How to run code
Go to the Main.py. If you are running the code on Windows, You will need to change line 29 by removing the "../" from the filepath. 
You will also need to change this line to read in the other input files. Then run the Main.py file and it will complete a full run.