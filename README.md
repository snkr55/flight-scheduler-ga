# Genetic Algorithm: Flight Scheduler 

## Problem Statement

Six people are traveling from six different cities — **Lisbon, Dublin, Madrid, Brussels, London, and Paris** — to a common destination, **Rome**, to attend a meeting and group activity.  

Each person has multiple flight options for both **outbound** (to Rome) and **return** (from Rome) trips, all at different timings and costs.

They want to:

- **Arrive in Rome in time for the meeting and start together**
- **Return from Rome together**, ensuring they reach the airport before the earliest flight departs
- **Minimize total waiting time** (at Rome airport for both arrival and departure)
- **Minimize the total flight cost** for all travelers

## Objective

The goal is to find an **optimized flight schedule** for all travelers that minimizes:

- **Total cost** of all flights (outbound + return)
- **Total waiting time** (for both arrival and departure windows)

This is a classic **multi-objective optimization problem**, solved using a **Genetic Algorithm**.

## Genetic Algorithm Approach

The Genetic Algorithm (GA) is inspired by natural selection, using:

- **Initial population**: Randomly generated flight schedules
- **Fitness function**: Evaluates total cost and total waiting time
- **Selection**: Chooses the best solutions based on fitness
- **Crossover**: Combines pairs of solutions to create new ones
- **Mutation**: Introduces slight changes to maintain diversity

## Data Overview

Each person has:

- A list of **outbound flights** to Rome
- A list of **return flights** from Rome

Each flight includes:

- Departure time
- Arrival time
- Cost

## Output

The GA produces:

- An optimal or near-optimal flight schedule
- Tabular summary of selected flights per person
- Total cost, total waiting time, and fitness score

## Example Output
![image](https://github.com/user-attachments/assets/9cece592-f0b0-463f-8b7b-586e832cfcfe)

