""" A random search algorithm, enter the amount of random searches you would like the algorithm to do, it will then perform the amount of random serches entered nd return the best solution found """

# Import required libraries 
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from random import shuffle
from operator import itemgetter
import math 

###########Functions#################

##### 1. Setup Functions: These Functions read the data and create datasets of various sizes #####

#Takes in the file name returns files size and a list  of colours. 
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

#Takes only the first n colours in the file 
def take(dataset, size):
	n_colours = []
	for i in range(size):
		n_colours.append(dataset[i])
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

#generates n random solutions to be evaluated
def random_searchs(solution,size_of_pop):
	x = 0
	r_searchs = []
	while x < size_of_pop:
		shuffle(solution)
		search = []
		for i in solution: 
			search.append(i)

		r_searchs.append(search)
		x = x + 1
	return r_searchs

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

#######SET STOPPING CRITERIA AND CHOOSE COLOUR SAMPLE######
number_of_searches = 70000 #Number of random searches to perform
sample = data  #Select data for 1000 colour sample data_hundred for the 100 colour sample and data 10 for the 10 colour sample

#Setting the permutations important for graphing
if sample == data:
	per = permutations
if sample == data_ten:
	per = permutations_ten
if sample == data_hundred:
	per = permutations_hundred

###### Main ######
searchs = random_searchs(sample,number_of_searches) #create a list of random soloutions
evaluated_searches = [] #create an empty list to store my random solutions after they have been evaluated 

for i in searchs: #evaluate the random searches
	fit = evaluate(i)
	evaluated_searches.append(fit)

evaluated_searches = sorted(evaluated_searches, key = itemgetter(-1)) #sort the evaluated serches by euchlidian distance, smallest echlidian distance on top


print("Solution: ", evaluated_searches[0][0], " Echlidian Distance: ", evaluated_searches[0][1]) #Print best score		
print()
	
plot_colours(evaluated_searches[0][0], per) #display solution graphicly 

