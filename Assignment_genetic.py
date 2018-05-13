""" A genetic algorithm, enter the initial population size, the number of generations you would like the algorithm to run for and it will return the best solution on screen along with the sorted colour chart"""

# Import required libraries 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from random import randint
from random import shuffle
from random import sample
from operator import itemgetter
import math 

###########Functions#################

##### 1. Setup Functions: These Functions read the data and create datasets of various sizes #####

#Takes in the file name returns files size and a dataframe of colours. 
def read_file(file):
 	with open (file, "rU") as cfile:
 		lines  = cfile.readlines()
 	f_size = lines[0]
 	data = lines[1:]
 	colours = []
 	for colour in data:
 		colour = colour.split(" ")
 		colour = list(map(float, colour))
 		colours.append(colour)
 	
 	return f_size, colours

#Takes only the first n colours in the file please note index starts at 1
def take(solution, size):
	n_colours = []
	for i in range(size):
		n_colours.append(solution[i])
	return n_colours

##### 2 Algorithm: These Functions are all needed for the random search algorithm #####

#Generates an initial starting population, takes in a data set and a population size 
def populate(solution,size_of_pop):
	x = 0
	population = []
	while x < size_of_pop:
		shuffle(solution)
		person = []
		for i in solution:
			person.append(i)

		population.append(person)
		x = x + 1
			

	return population

#Finds the sum echlidian distance of a solution 
def evaluate(solution):
	Sum_echlidian_dist = 0
	#For to find the sum echlidian distance for the solution
	for i in range(len(solution) - 2):
		place1 = solution[i]
		place2 = solution[i + 1]
		red1 = place1[0]
		red2 = place2[0]
		green1 = place1[1]
		green2 = place2[1]
		blue1 = place1[2]
		blue2 = place2[2]

		echlidian_dist = math.sqrt(math.pow(red1 - red2,2) + math.pow(green1 - green2,2) + math.pow(blue1 - blue2,2))
		Sum_echlidian_dist = Sum_echlidian_dist + echlidian_dist
	return solution, Sum_echlidian_dist


#A tournement to decide the parent solutions 
def tournament(population, rounds):
	parent = "Null" #Initially parent is null
	for i in range(rounds): #We select the number of rounds for the tournement the more rounds the more likley the solution with the lowest score will become the parent 
		x = randint(0,len(population) - 1) #Create a random integer this will be the index of the candidate
		candidate = population[x]
		if parent == "Null" or candidate[-1] > parent[-1]: #If parent is currently null or candidata has a lower euchlidian score than the current parent the candidate becomes the parent
			parent = candidate
	return parent


#Creates a 2 child solutions by combining the two parent solutions 
def recombination(parent1,parent2):
	l = len(parent1[1]) 
	x = randint(1,l) #Create a location to split the parents
	child1 = [] #Create two empty lists for the new children
	child2 = []
	i = 0
#child 1 gets the first part of its solution from parent1 and the second part from parent 2 and vice versa for child2
	while i < l:
		if i <= x:
			child1.append(parent1[1][i])  
			child2.append(parent2[1][i])

		if i > x:
			if parent2[1][i] not in child1:
				child1.append(parent2[1][i])
			if parent1[1][i] not in child2:
				child2.append(parent1[1][i])

		i = i + 1

	for i in parent1[1]:
		if i not in child1:
			child1.append(i)

	for i in parent2[1]:
		if i not in child2:
			child2.append(i)
	
	return child1,child2

	

#Randomly mutate solution 
def random_mutation(solution):
#Inverts solution creating a random 2 flip neighbour
	pos1 = randint(0, len(solution)-1) 
	pos2 = randint(0,len(solution )-1)
	if pos1 < pos2:
		solution[pos1:pos2] = solution[pos1:pos2][::-1]
	if pos2 < pos1:
		solution[pos2:pos1] = solution[pos2:pos1][::-1]
	mutated_data = solution
	
	return mutated_data

	
  
#Function takes in a list of solutions finds the solution with the lowest echlidian disatance and returns it 
def sort_list(solutions):
	best_sol = solutions[0][0:-1]
	best_dist = solutions[0][-1]
	for i in range(len(solutions) - 1):
		if solutions[i][-1] < best_dist:
			best_dist = solutions[i][-1]
			best_sol = i
	return best_sol, best_dist


#### 3 Display: Functions needed to display final output as a picture #####

# Display the colours in the order of the permutation in a pyplot window 
def plot_colours(colours, permutation):

	assert len(colours) == len(permutation)
	
	ratio = 10 # ratio of line height/width, e.g. colour lines will have height 10 and width 1

	img = np.zeros((ratio, len(colours), 3))

	for i in range(0, len(colours)):
		img[:, i, :] = colours[permutation[i]]

	fig, axes = plt.subplots(1, figsize=(8,4)) # figsize=(width,height) handles window dimensions
	axes.imshow(img, interpolation='nearest')
	axes.axis('off')
	plt.show()



######### Setup #######
data = read_file("C:\\Users\\Glenn's pc\\Documents\\Uni\\ITNPBD8\\Assignment\\colours.txt") #Read in data file

#Create 3 data sets,10, 100 and 1000 colour datasets
f_size = data[0]
data = data[1] #1000 colour sample
size = len(data)
permutations = np.arange(size) #important for visulization 

data_ten = take(data,10) #10 colour sample
size_ten = len(data_ten)
permutations_ten = np.arange(size_ten)
#print(evaluate(data_ten))
#print()
#plot_colours(data_ten, permutations_ten)

data_hundred = take(data,100) #100 colour sample
size_hundred = len(data_hundred)
permutations_hundred = np.arange(size_hundred)

### Select the algorithms parameters
population_size = 50 #size of the population
generations = 20000 #How many generations should the algorithm run for 
sample = data #Select the colour sample to use 1000 colour sample = data, 100 colour sample = data_hundred,  10 colour sample = data_ten

#Setting the permutations important for graphing
if sample == data:
	per = permutations
if sample == data_ten:
	per = permutations_ten
if sample == data_hundred:
	per = permutations_hundred

###### Main ######
population = populate(sample, population_size) #Generate a random initial population 
population_dist = [] # A variable that will store solutions and their euchlidian score

#A for loop to evaluate each member of the population and append the solution and evaluation onto the population_dist list 
for i in population:
	person = evaluate(i) #evaluate each individual in the population
	population_dist.append(["Solution: ", person[0], " Echlid Dist: ", person[1]])

gen = 0
while gen < generations:

#Two parents are created through tournament selection
	parent1 = tournament(population_dist,int(len(population_dist)/2))
	parent2 = tournament(population_dist,int(len(population_dist)/2))

#The two parents are combined to make children these child solutions are then mutated, evaluated and replace the worst two exising solutions
	children = recombination(parent1,parent2) #create two children by merging parent solutions
	child1 = children[0] #create the variable to hold child solution 1
	child2 = children[1] #create the variable to hold child solution 2
	child1 = evaluate(child1) #Evaluate the two child scores
	child2 = evaluate(child2) 
	child1 = ["Solution: ", child1[0], " Echlid Dist: ", child1[1]] #Set the two child solutions to the same format as the population solutions 
	child2 = ["Solution: ", child2[0], " Echlid Dist: ", child2[1]]
	population_dist = sorted(population_dist, key = itemgetter(3)) #Sort the list of population solutions so the solution with the lowest euchlidian distance is at the top of the list
	echlidian = population_dist[0][3] #Here to help graph echlidian distance over a generation
	del population_dist[-2:] #Delete the worst two solutions from the list
	population_dist = population_dist + [child1] + [child2] #Add the two child solutions to the population list 
	

	gen = gen + 1 #increase the generation counter

population_dist = sorted(population_dist, key = itemgetter(3)) #sort the population by echlidian distance (smallest on top)
print(population_dist[0]) #print best solution and echlidian distance
print()


plot_colours(population_dist[0][1], per) #show sorted colour chart
