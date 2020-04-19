# Winning the Lottery with Python

This was completed when I was first learning Python.  

This is my attempt to guess winning numbers for the lottery. This particular lottery is played in Brazil ("Lotomania") and has simple rules:
  1. Each player picks 50 integers between 00 and 99
  2. 20 numbers are drawn in the lottery
  3. If a player matches between 15 and 20 numbers, he wins a prize

I wrote a script in Python that simulates this lottery 10,000 times with 20 'winning' numbers drawn at random, which I reference to as a "winning vector" as well as the same number of "winning draws" of 50 numbers that include all 20 winning numbers, as well as an additional 30 random numbers, from each simulated game.

# Randomness
Because I assumed this is all random, I don't think any solution drawn here will guarantee a win. In fact, this fares no better than just selecting any 50 numbers at random. In short, this project is **just for fun**.  

# Historical data
If I had a large selection of historical winning vectors, I could test the assumption that numbers are really being drawn at random. If I found that they were not, I could construct a simulation method to mirror the nature of the non-random draws, whatever that was.  

# Requirements
Python 3

# Testing validity of solution
Since the script iterates through so many simulations to come up with an answer, I thought it important to test that the solution worked. To do that, I wrote this function that returns errors if the winning solution had something wrong -- e.g. incorrect vector size, elements in an incorrect format (float instead of int), numbers that were too big or too small, etc. And this function adapts to different lottery rules.
```python
def Lottery(tup):
    global draws, lowest, highest # Get parameters globally - no global parameters, everything else fails
    if type(tup) != tuple:
        try: tup = tuple(tup) # Needs to be tuple or something that can easily be transformed into a tuple
        except: return TypeError('Expecting tuple, got {}'.format(type(tup)))
    for el in tup:
        if type(el) != int:
            try: int(el) # Elements in tuple need to be integers or something that can easily become integers
            except: return TypeError('All elements must be integers! No {}, which is {}.'.format(el, type(el)))
        if el < lowest:
            return TypeError('Integers can\'t be less than {}, got {}'.format(lowest, el))
        if el > highest:
            return TypeError('Integers can\'t be greater than {}, got {}'.format(highest, el))
    if len(tup) != draws:
        return TypeError('Expecting {} integers, got {}'.format(draws, len(tup)))
    tup_dups = []
    for num in tup:
        if num not in tup_dups:
            tup_dups.append(num) # Testing for duplicates in tuple - can't have that
        else: return TypeError('Duplicates found')
    else: return tup  # If everything is fine, return whatever was put in 
```
# Required libraries
The following imports are necessary:
```python
import platform
import numpy as np
import collections
import pandas as pd
from collections import defaultdict
from statistics import mean, median, mode, stdev, variance
```
# Sorting the vectors
Important to this analysis was sorting each randomly generated winning vector of 20 integers so that the smallest number is in the first position, the largest in the last. That way, I could do summary statistics on each integer's position and better predict what each number should be. The same applies to randomly generated winning draws of 50 integers. This allowed me to predict a mean, median, min, max, and standard deviation of each integer based on its position and create hypothetical winning draws.

```python
# Generate winning vectors of 20 integers sorted - in a dictonary
# Keyword is the simualation number (game0, game100, etc.), value is the sorted vector of 20
winners = {}
for i in range(sim):
    winners['game{}'.format(i)] = list(np.sort(np.random.choice(range(lowest, highest+1), 20, replace = False)))

# Generate winning draws of 50 integers sorted
winning_draws = {}
for k in winners:
    winning_draws[k] = winners[k]
    remaining = []
    for el in range(lowest, highest+1):
        if el not in winners[k]:
            remaining.append(el)
    remainder_list = list(np.random.choice(remaining, (draws - matches), replace = False)) # Subtract matches from draws so that you only select the remaining number of numbers allowed, no more
    for num in remainder_list:
        winning_draws[k].append(num)
    winning_draws[k] = list(np.sort(winning_draws[k]))
```
# Running 3 different solutions
I came up with three different potential solutions. Any one of these solutions could be rerun any number of times to derive different vectors if you were planning on playing more than one ticket.

## Option 1
Take the min, max, and a random sample of medians from the aggregated winning vectors, which are each ordered from lowest to highest integer value. Why use this method? Because it's a good way to scrape around all the possible outcomes -- doesn't skew too much to the middle neither to the edges of a potential winner: 
```python
# Parse values from dictionaries
opt_1 = []
for k in mins:
    opt_1.append(mins[k])

for k in maxes:
    if maxes[k] not in opt_1:
        opt_1.append(maxes[k])

remaining_medians = []
for k in medians:
    if medians[k] not in opt_1:
        remaining_medians.append(medians[k])

opt_1_remaining = np.random.choice(remaining_medians, draws - len(opt_1), replace = False)

for num in list(opt_1_remaining):
    opt_1.append(num)

# Does this solution work? - if no errors, then yes
print(np.sort(Lottery(opt_1)))
```
## Option 2
Take the mean value of the aggregated winning vectors ordered from lowest to highest integer value:
```python
# Simulate winning draws
winning_draws = {}
for k in winners:
    winning_draws[k] = winners[k]
    remaining = []
    for el in range(lowest, highest+1):
        if el not in winners[k]:
            remaining.append(el)
    remainder_list = list(np.random.choice(remaining, (draws - matches), replace = False))
    for num in remainder_list:
        winning_draws[k].append(num)
    winning_draws[k] = list(np.sort(winning_draws[k]))

# Get mean of winning draws
winning_means = {}
for i in range(draws):
    el = []
    for h in range(sim):
        el.append(winning_draws['game{}'.format(h)][i])
    winning_means['sel-{:>02}'.format(i)] = int(round(mean(el), 0))

# View the mean
print(collections.OrderedDict(sorted(winning_means.items())))

opt_2 = [] # Create an empty list to be filled with the mean of each selection location for winning draws
for k in winning_means:
    opt_2.append(winning_means[k])

# Does option 2 work?
print(np.sort(Lottery(opt_2)))
```
## Option 3
Take the most frequently selected values from the winning vectors:
```python
all_winners = []
for k in winning_draws:
    for num in winning_draws[k]:
        all_winners.append(num)

# Count how many times each number was selected in the winning draws
index_freq = []
for i in range(lowest, highest+1):
    index_freq.append(all_winners.count(i))

# Create a dataframe with this info -- easier to access than a dictionary in this case
winners_df = pd.DataFrame(index = range(lowest, highest+1))
winners_df['pick'] = range(lowest, highest+1)
winners_df['freq'] = index_freq
print(winners_df.head(20))

# Sort by the picked numbers of highest frequency
winners_df = winners_df.sort_values(by = ['freq'])
winners_50 = winners_df[0:50]
# Get your winning numbers
opt_3 = winners_50['pick']

# Does option 3 work?
print(np.sort(Lottery(opt_3)))
```
# Results:
The following are results from each solution:
## Option 1
```python
[ 0  1  2  3  4  6  8  9 12 13 14 16 17 22 24 26 27 28 31 32 37 42 46 47 51
 52 53 54 55 57 59 61 62 67 74 76 77 79 82 83 86 89 92 93 94 95 96 97 98 99]
```
## Option 2
```python
[ 0  2  4  6  8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48
 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98]
 ```
 ## Option 3
```python
[ 0  5  6  7  8  9 12 13 17 20 21 22 23 27 28 30 32 34 35 40 42 43 45 46 48
 49 53 54 57 59 60 61 62 63 71 72 73 74 76 77 78 81 82 84 86 89 94 95 98 99]
 ```
 
