import sys
import time
import random
import math



# ==================== AIRPORT CODES ===================

# To define people and airport codes

people = [('Lisbon','LIS'),
          ('Paris','CDG'),
          ('London','LHR'),
          ('Madrid','MAD'),
          ('Dublin','DUB'),
          ('Brussels','BRU')]
destiny = 'FCO' # Rome



# ==================== FLIGHTS DATASET ===================

# To store flights.txt file in the format of a dictionary
# Sample flights dictionary format: flights{(origin, destiny):[departure, arrival, price]}

flights = {}
for row in open(r"C:\Users\DELL\Documents\Personal\PORTFOLIO\Genetic-Algorithm\Flight-Schedule\flight-scheduler-ga\flights.txt"):
    origin, destiny, departure, arrival, price = row.split(',')
    flights.setdefault((origin, destiny),[])
    flights[(origin,destiny)].append((departure,arrival,int(price)))
#flights
#flights[('FCO', 'LIS')]



# ==================== PRINT SCHEDULE ===================

# This function takes a schedule as input and prints the outbound and inbound flight details for each person
# There are 6 people, and each person takes 2 flights (outbound and inbound).
# Hence the schedule has 12 flights in total.
# The first pair indicates the outbound and inbound flights for the first person, the second pair for the second person, and so on.
# These nubers represent the index of the flight in the flights dictionary, for that respective route.
# Since, in the given dataset, each route has 10 flights, the index of the flight can be between 0 and 9.
# Thus, the schedule is a list of 12 integers, each between 0 and 9.
# Sample schedule format: [1,3, 4,5, 7,2, 8,6, 3,9, 2,5]


def print_schedule(schedule, display_schedule_and_price=True):
    # If display_schedule is True, print flight schedule details; if False, only return total price
    flights_id = -1
    total_price = 0
    for i in range(len(schedule) // 2):
        # For each person, we will get the outbound and inbound flights according to the given schedule
        origin = people[i][1]
        name = people[i][0]
        flights_id += 1
        outbound = flights[(origin,destiny)][schedule[flights_id]]
        flights_id += 1
        inbound = flights[(destiny,origin)][schedule[flights_id]]
        # To check the outbound and inbound flights for each person
        #print(name)
        #print('Outbound:', outbound)
        #print('Inbound:', inbound)
        # To print the flight details in formatted way
        if display_schedule_and_price == True:
            print(f'{name:10} | {origin:3} | OUTBOUND: {outbound[0]:5}-{outbound[1]:5} ${outbound[2]:3} | INBOUND: {inbound[0]:5}-{inbound[1]:5} ${inbound[2]:3}')
            print('-' * 74)
    
        # To calculate the total price for the given schedule
        total_price += outbound[2] + inbound[2]
        
    # To print the total price for the given schedule
    if display_schedule_and_price == True:
        print(f'TOTAL PRICE: ${total_price}')          
            
    return total_price

# To check the print_schedule function
#print_schedule([1,3, 4,5, 7,2, 8,6, 3,9, 2,5])
#flights[('LIS','FCO')]



# ==================== TIME CONVERSION ===================

# This function takes a time in HH:MM format and converts it to minutes
# Sample time format: '12:30'

#t = time.strptime('12:30', '%H:%M')
#print(t)
#print(t[3], t[4], t[3]*60+t[4])

def get_minutes(hour):
    t = time.strptime(hour, '%H:%M')
    return t[3]*60+t[4]

# To check the get_minutes function
#get_minutes('12:30')



# ==================== FITNESS FUNCTION ===================

# This function takes a schedule as input and calculates the fitness score based on the following criteria:
# 1. The total price of all the flights in the schedule.
# 2. The total wait time for all the people in the group, for both outbound and inbound flights.

def fitness_function(schedule):

    # PART-1: To calcualte the total price of all the flights in the given schedule and to identify the last arrival and first departure time
     
    flights_id = -1
    total_price = 0
    last_arrival = get_minutes('00:00')
    # Initialize last_arrival with the earliest possible time of the day (00:00)
    # This ensures that any flight arrival time will be later than this initial value.
    # This is to ensure that the last_arrival variable is updated with the latest arrival time of the given schedule.
    first_departure = get_minutes('23:59')
    # Initialize first_departure with the latest possible time of the day (23:59)
    # This ensures that any flight departure time will be earlier than this initial value.
    # This is to ensure that the first_departure variable is updated with the earliest departure time of the given schedule.

    # We use the last arrival time to calculate total group waiting time at the destination.
    # A later arrival means more waiting. Similarly, the first departure time is used for the return,
    # as everyone must arrive early for the first departure — earlier departures mean longer waits.


    for i in range(len(schedule) // 2):
        # For each person, we will get the outbound and inbound flights according to the given schedule
        origin = people[i][1]
        flights_id += 1
        outbound = flights[(origin,destiny)][schedule[flights_id]]
        flights_id += 1
        inbound = flights[(destiny,origin)][schedule[flights_id]]
        # To calculate the total price for the given schedule
        total_price += outbound[2] + inbound[2]
        # To update the last arrival time with the latest arrival time of the given schedule
        if last_arrival < get_minutes(outbound[1]):
            last_arrival = get_minutes(outbound[1])
        # To update the first departure time with the earliest departure time of the given schedule
        if first_departure > get_minutes(inbound[0]):
            first_departure = get_minutes(inbound[0])

    # To check the total price, last arrival and first departure time for a given schedule and validate the fitness function
    #print('Total Price:', total_price)
    #print('Last Arrival:', last_arrival)
    #print('First Departure:', first_departure)
    
    # PART-2: To calcualte the total wait time for all the people in the group, for both outbound and inbound flights

    total_wait_time = 0
    flights_id = -1
    for i in range(len(schedule) // 2):
        # Again, for each person, we will get the outbound and inbound flights according to the given schedule
        origin = people[i][1]
        flights_id += 1
        outbound = flights[(origin,destiny)][schedule[flights_id]]
        flights_id += 1
        inbound = flights[(destiny,origin)][schedule[flights_id]]
        # To calculate the wait time for the given schedule
        total_wait_time += last_arrival - get_minutes(outbound[1])
        total_wait_time += get_minutes(inbound[0]) - first_departure
        # These lines calculate each traveler’s waiting time at the airport and add it to the running total wait time.
        # It sums the difference between the latest arrival and each traveler's arrival,
        # and the difference between each traveler's departure and the earliest departure time.

    return total_price + total_wait_time

# To check if the fitness_fucntion is calculating total price, lsat arrival and first departure correctly

#print(fitness_function([1,3, 4,5, 7,2, 8,6, 3,9, 2,5]))
#print_schedule([1,3, 4,5, 7,2, 8,6, 3,9, 2,5])
#print(get_minutes('21:45')) # the last arrival time for the above schedule
#print(get_minutes('9:58')) # the first departure time for the above schedule



# ==================== DOMAIN ===================

# In the context of genetic algorithms, the domain defines the possible values that each "gene" in an "individual" can take.
# The domain is a list of tuples, where each tuple represents the range of valid values for each gene.

# To check the number of flights for each route in the flights dictionary
#for route in flights:
    #print(f"Route {route}: {len(flights[route])} flights")

# Here, the domain is set to (0, 9) because, in flights.txt file, each route has 10 flight options.
#domain = [(0,9)] * (len(people)*2)
#domain
# In a real-world scenario, the domain should be dynamically determined based on the actual number of flights per route, as this can vary.

domain = []
for person in people:
    origin = person[1]
    # Outbound
    domain.append((0, len(flights[(origin, destiny)]) - 1))
    # Inbound
    domain.append((0, len(flights[(destiny, origin)]) - 1))
#domain



# ==================== MUTATION FUNCTION ===================

# Mutation is one of the genetic operators used in genetic algorithms to maintain genetic diversity from one generation of a population of genetic algorithm chromosomes to the next.
# The mutation function randomly selects a gene in the schedule and changes it to a new random value within the domain.
# This introduces variability into the population, allowing the algorithm to explore new solutions.
# The mutation rate determines how often mutations occur.
# The mutation rate is set to 0.1, meaning there is a 10% chance of mutation for each gene in the schedule.

def mutation(domain, schedule, mut_prob):
    mutant = schedule
    if random.random() < mut_prob: # Mutation probability check; random.random() generates a float between 0.0 and 1.0; only if it's less than mut_prob, mutation occurs
        gene = random.randint(0, len(schedule) - 1) # Randomly select a gene index in the schedule
        #print(gene) # To check which gene is selected for mutation
        # If the selected gene value is not at the boundary of its domain, we can mutate it by incrementing or decrementing its value
        
        if schedule[gene] > domain[gene][0] and schedule[gene] < domain[gene][1]: # Check if the gene is not at the boundaries of its domain
            # Can increment or decrement; pick randomly
            if random.random() < 0.5:
                mutant = schedule[0:gene] + [schedule[gene]+1] + schedule[gene+1:]
            else:
                mutant = schedule[0:gene] + [schedule[gene]-1] + schedule[gene+1:]
        elif schedule[gene] == domain[gene][0]: # Check if the gene is not at the lower boundary of its domain
            # Only increment
            mutant = schedule[0:gene] + [schedule[gene]+1] + schedule[gene+1:]
        elif schedule[gene] == domain[gene][1]: # Check if the gene is not at the upper boundary of its domain
            # Only decrement
            mutant = schedule[0:gene] + [schedule[gene]-1] + schedule[gene+1:]
        #print('Mutation has occured!') # To indicate that mutation has occurred
    #else:
        #print('Mutation has not occured!') # To indicate that mutation has not occurred
    
    # The function returns the mutated schedule, which is either the original schedule or the mutated one.     
    return mutant

# To check the mutation function
#print(mutation(domain, [1,3, 4,5, 7,2, 8,6, 3,9, 2,5], 0.5))



# =================== CROSSOVER FUNCTION ====================

# Crossover is another genetic operator used in genetic algorithms to combine the genetic information of two parents to generate new offspring.
# The crossover function takes two parent schedules and combines them to create a new schedule. 
# The crossover point is randomly selected, and the genes from both parents are combined to create a new schedule.

def crossover(domain, individual1, individual2):
    gene = random.randint(1, len(domain)-2) # Randomly select a crossover point, ensuring it's not the first or last gene
    #print(gene) # To check which gene is selected for crossover
    return individual1[0:gene] + individual2[gene:] # Combine the first part of individual1 with the second part of individual2 to create a new schedule

# To check the crossover function
#print(crossover(domain, [1,3, 4,5, 7,2, 8,6, 3,9, 2,5], [0,2, 5,6, 8,1, 9,7, 4,3, 6,0]))



# =================== GENETIC ALGORITHM ====================

# STEP-1: Initialize the population with random schedules (individuals)
# STEP-2: Evaluate the fitness of each individual in the population
# STEP-3: Select the best (eilite) individuals based on their fitness scores (Elitism)
# STEP-4: Perform crossover and mutation to create new individuals
# STEP-5: Replace the old population with the new population
# STEP-6: Repeat steps 2-5 until a stopping condition is met (e.g., a maximum number of generations)

def genetic_algorithm(domain, fitness_function, population_size=100, elitism = 0.2, generation=100, mut_prob=0.05):
    
    # 1: Initialize the population with random schedules (individuals)
    
    population = []
    for i in range(population_size):
        individual = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
        population.append(individual)
        #print(individual)
    #print(population)

    # 2: Evaluate the population and select elite individuals based on their fitness scores

    elitism_count = int(population_size * elitism) #  To calculate the number of elite individuals based on the elitism rate
    #print(elitism_count)
    for i in range(generation):
        solutions = [(fitness_function(individual), individual) for individual in population]
        # This line calculates the fitness score for each individual in the population and creates a list of tuples containing the fitness score and the individual.
        solutions.sort()
        # This line sorts the solutions based on their fitness scores in ascending order, so the best solutions (lowest fitness scores) come first.
        #print(solutions)
        ordered_individuals = [individual for (fitness, individual) in solutions]
        # This line extracts the individuals from the sorted solutions, discarding their fitness scores.
        #print(ordered_individuals)
        population = ordered_individuals[:elitism_count]
        # This line keeps only the elite individuals in the population, based on the elitism count calculated earlier.
        #print(population)

        # 3: Perform crossover and mutation to create new individuals for the remaining (population_size - elitism_count) individuals

        while len(population) < population_size:
            i1 = random.randint(0, elitism_count-1) # Randomly select an index for the first parent from the elite individuals
            i2 = random.randint(0, elitism_count-1) # Randomly select an index for the second parent from the elite individuals
            #print(i1, i2, population[i1], population[i2]) # To check which parents are selected for crossover
            # Perform crossover between the two selected parents to create a new individual
            new_individual = crossover(domain, population[i1], population[i2])
            #print('New Crossover Individual:', new_individual)
            # Perform mutation on the new individual with the given mutation probability
            new_mutant_individual = mutation(domain, new_individual, mut_prob)
            #print('New Mutant Individual:', new_mutant_individual)
            population.append(new_mutant_individual)
            # This line appends the new mutant individual to the population, ensuring that the population size remains constant.
        #print('Generation: ', i+1, population[0], 'Best Fitness:', fitness_function(population[0]))
        # This line prints the current generation number, the best individual in the population, and its fitness score.     

    return solutions[0][1] # Return the best individual from the final population, which has the lowest fitness score



# =================== EXECUTION OF GENETIC ALGORITHM ====================

best_schedule = genetic_algorithm(domain, fitness_function, population_size=100, elitism=0.2, generation=500, mut_prob=0.05)

# To print the best schedule found by the genetic algorithm
print('Best Schedule:', best_schedule)

# To print the fitness score for the best schedule
print('FITNESS SCORE:', fitness_function(best_schedule))

# To print the flight details for the best schedule
print_schedule(best_schedule)

# To print total wait time for the best schedule
total_wait_time_minutes = fitness_function(best_schedule) - print_schedule(best_schedule, display_schedule_and_price=False)
hours = total_wait_time_minutes // 60
minutes = total_wait_time_minutes % 60
print(f'TOTAL WAIT TIME: {hours} hours {minutes} minutes')
