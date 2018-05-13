""" Iterative local search algorithm, enter the hill climb stopping criteria, the number of iterations you would like the algorithm to perform and a colour sample
the program will return a best solution and a sorted colour chart"""

# Import required libraries 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import randint
from random import shuffle
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



def hill_climb(solution):
	x = 0
	result_dist = 100000
	while x < hill_climb_stop: #Stopping criteria when x reaches 10,000
#I create an initial solution and initial evaluation
		init_evaluation = evaluate(solution)
		init_dist = init_evaluation[-1]
#Produce a random neighbour and evaluate it 
		neighbour = random_mutation(solution)
		neighbour_evaluation = evaluate(neighbour)
		neighbour_dist = neighbour_evaluation[-1]

#Compair with best solution if the euchlidian distance is less than current best solution the neighbour becomes the best solution 
		if init_dist <= neighbour_dist:
			test = solution
			test_dist = init_dist

		if neighbour_dist < init_dist:
			solution = neighbour
			test = neighbour
			test_dist = neighbour_dist

		if test_dist <=  result_dist:
			result = test 
			result_dist = test_dist

		
		x = x + 1
	return result, result_dist


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
data = read_file("ENTER DATA PATH HERE") #Read in data file

#Create 3 data sets,10, 100 and 1000 colour datasets
f_size = data[0]
data = data[1] #1000 colour sample
size = len(data)
permutations = np.arange(size) #important for visulization 

data_ten = take(data,10) #10 colour sample
size_ten = len(data_ten)
permutations_ten = np.arange(size_ten)


data_hundred = take(data,100) #100 colour sample
size_hundred = len(data_hundred)
permutations_hundred = np.arange(size_hundred)


#####Select the Algorithms parameters
sample = data #Chose the sample to run the algorithm on the 10 colour sample is data_ten the 100 Colour sample is data_hundred and the 1000 colour sample is data
hill_climb_stop = 10000 #Stopping criteria for the hill climb algorithm
iterations = 100 #Number of times local search should iterate 

#Setting the permutations important for graphing
if sample == data:
	per = permutations
if sample == data_ten:
	per = permutations_ten
if sample == data_hundred:
	per = permutations_hundred
###### Main ######
initial_solution = random_mutation(sample) #Create a randomly generated solution
solution = hill_climb(initial_solution) #preform a hill climb on the inital solution to get our baseline best solution and best echlidian distance 
best_solution = solution[0] #This is the best solution from the inital hill climb
best_dist = solution[1] #This is the echlidian distance for the best solution 
x = 0
while x < iterations:
	mutate_sol = random_mutation(best_solution) #randomly mutate our best solution
	#mutate_sol = random_mutation(mutate_sol) #Then mutate it again, the point of this is to search more of the search space and avoid getting stuck in local minimums however this process cannot guarentee that the algorithm can escape all local minimums
	rival_solution = hill_climb(mutate_sol) #preform a hill climb on the mutated solution
	rival_sol = rival_solution[0] #This is the best solution from the previous hill climb
	rival_dist = rival_solution[1] #This is the echlidian distance for the best solution from the previous hill climb 

	if best_dist <= rival_dist:
		result = best_solution
		result_dist = best_dist

	if rival_dist < best_dist:
		result = rival_sol
		result_dist = rival_dist
		best_solution = rival_sol
		best_dist = rival_dist
	
	x = x + 1

print(result_dist) #print out best soloution an its echlidian distance print("Solutions: ",result," Echlidian Distance", result_dist)

plot_colours(result, per) #return sorted colour charts

	



