# Colour-Sorting-algorithms-
4 Algorithms that sort a list of colours
Algorithms are:

1. Random Search 
2. Hill Climber
3. Iterative Local Search 
4. Genetic Algorithm

There is also 1 data file:
1. colours.txt

This repository includes the 4 algorithms and a colour file to test them.

Each algorithm in the assignment has its own .py file each is labeled clearly but for ease:
Hill climb = Assignment_hill_climber.py
Random search = Assignment_rand_search.py
Iterative local search = Assignment_iterative_local_search.py
Genetic Algorithm = Assignment_genetic.py
Report = Assignment report final.pdf

Using the programms themselves:

Each program has three data sets the 10,100 and 1000 colour sample sets, by default the programms are all set to run on the 1000 colour 
sample data set but this can be changed by altering the sample variable within the proggram.  The sample variable has 3 possible values:
sample = data_ten   selects the 10 colour sample
sample = data_hundred   selects the 100 colour sample
sample = data    selects the 1000 colour sample

If you don't need to change anything and just run the program it will select the 1000 colour data sample it will run the algorithm on the 
1000 colour sample until it meets the stopping criteria, then the program will print out the solution and the solutions sum echlidian 
distance score, aswell as printing the actual colour chart for the best solution. 
