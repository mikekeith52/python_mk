
# coding: utf-8

# In[1]:


# View python version
import platform
print('This is python version {}'.format(platform.python_version()))
# I'm using version 3.4.5


# In[2]:


# Import libraries
import numpy as np
import collections
import pandas as pd


# In[3]:


from collections import defaultdict
from statistics import mean, median, mode, stdev, variance


# In[4]:


import random
# Set random seed for replicable results
random.seed(20)


# In[5]:


# Set global parameters
draws = 50 # 50 draws
matches = 20 # 20 matches to win
lowest = 0 # Cannot be lower than 0
highest = 99 # Cannot be higher than 99
sim = 10000 # Number of simulations of the game


# In[6]:


def Lottery(tup):
    global draws, lowest, highest # Get parameters globally - no gloabl parameters, everything else fails
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


# In[7]:


# Test some of the errors
test = list(range(49))
Lottery(test)
test.append(30)
Lottery(test)
# Test if it works
print(Lottery(range(50)))


# In[8]:


# Simulate winning vectors `sim` times
winners = {}
for i in range(sim):
    winners['game{}'.format(i)] = list(np.sort(np.random.choice(range(lowest, highest+1), 20, replace = False)))


# In[9]:


# Check to make sure it worked
print(winners['game0'], winners['game500'],  winners['game9000'])


# In[10]:


# View the distribution of the winning vectors by ordered element
# sel-00 is the lowest number of each winning vector, sel-19 is the highest
means = {} # Create empty dictionaries
medians = {}
modes = {}
mins = {}
maxes = {}
sds = {}
varrs = {}
for i in range(matches):
    el = []
    for h in range(sim):
        el.append(winners['game{}'.format(h)][i])
    means['sel-{:>02}'.format(i)] = int(round(mean(el), 0))
    medians['sel-{:>02}'.format(i)] = int(round(median(el), 0))
    try: modes['sel-{:>02}'.format(i)] = mode(el) 
    except: modes['sel-{:>02}'.format(i)] = None
    mins['sel-{:>02}'.format(i)] = min(el)
    maxes['sel-{:>02}'.format(i)] = max(el)
    sds['sel-{:>02}'.format(i)] = round(stdev(el), 2)
    varrs['sel-{:>02}'.format(i)] = round(variance(el), 2)


# In[11]:


# Print the dictionaries ordered by selection number to see some summary statistics
print('means', collections.OrderedDict(sorted(means.items())))
print('medians', collections.OrderedDict(sorted(medians.items())))
print('mins', collections.OrderedDict(sorted(mins.items())))
print('maxes', collections.OrderedDict(sorted(maxes.items())))
print('sds', collections.OrderedDict(sorted(sds.items())))


# In[12]:


## Now to choose a winning vector of 50
# Option 1 - take the min, max, and sample of remaining medians - that way, you get the highest, lowest, and some in between for each selection
### Run the following all together for no confusion
opt_1 = []
for k in mins:
    opt_1.append(mins[k])
print('phase1:', opt_1) # Print after each phase to see progress

for k in maxes:
    if maxes[k] not in opt_1:
        opt_1.append(maxes[k])
print('phase2:', opt_1)

remaining_medians = []
for k in medians:
    if medians[k] not in opt_1:
        remaining_medians.append(medians[k])
print('remaining medians:', remaining_medians)

opt_1_remaining = np.random.choice(remaining_medians, draws - len(opt_1), replace = False)
print('sampled medians:', opt_1_remaining)

for num in list(opt_1_remaining):
    opt_1.append(num)

print('final:', opt_1)
####


# In[13]:


# Does this solution work? - if no errors, then yes
print(np.sort(Lottery(opt_1)))


# In[14]:


# Opt 2 - take mean/median of simulated winning draws
# Simulate winning vector picks `sim` times
# This is simulating random winning draws for each winning vector
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


# In[15]:


# Check to see that it worked
print(winning_draws['game1'], winning_draws['game1000'])


# In[16]:


# Get summary statistics for winning draws
winning_means = {}
winning_medians = {}
winning_modes = {}
winning_mins = {}
winning_maxes = {}
winning_sds = {}
winning_varrs = {}
for i in range(draws):
    el = []
    for h in range(sim):
        el.append(winning_draws['game{}'.format(h)][i])
    winning_means['sel-{:>02}'.format(i)] = int(round(mean(el), 0))
    winning_medians['sel-{:>02}'.format(i)] = int(round(median(el), 0))
    try: winning_modes['sel-{:>02}'.format(i)] = mode(el) 
    except: winning_modes['sel-{:>02}'.format(i)] = None
    winning_mins['sel-{:>02}'.format(i)] = min(el)
    winning_maxes['sel-{:>02}'.format(i)] = max(el)
    winning_sds['sel-{:>02}'.format(i)] = round(stdev(el), 2)
    winning_varrs['sel-{:>02}'.format(i)] = round(variance(el), 2)


# In[17]:


# View the mean
print(collections.OrderedDict(sorted(winning_means.items())))


# In[18]:


opt_2 = [] # Create an empty list to be filled with the mean of each selection location for winning draws
for k in winning_means:
    opt_2.append(winning_means[k])
print(opt_2)


# In[19]:


# Does option 2 work?
print(np.sort(Lottery(opt_2)))


# In[20]:


# Option 3 - pick the most-picked numbers from the winning vectors
all_winners = []
for k in winning_draws:
    for num in winning_draws[k]:
        all_winners.append(num)
print(all_winners[0:100])
print(all_winners[(sim-100):sim])


# In[21]:


# Count how many times each number was selected in the winning draws
index_freq = []
for i in range(lowest, highest+1):
    index_freq.append(all_winners.count(i))


# In[22]:


print(index_freq)


# In[27]:


# Create a dataframe with this info -- easier to access than a dictionary in this case
winners_df = pd.DataFrame(index = range(lowest, highest+1))
winners_df['pick'] = range(lowest, highest+1)
winners_df['freq'] = index_freq
print(winners_df.head(20))


# In[24]:


# Sort by the picked numbers of highest frequency
winners_df = winners_df.sort_values(by = ['freq'])
winners_50 = winners_df[0:50]
# Get your winning numbers
opt_3 = winners_50['pick']


# In[25]:


# Does option 3 work?
print(np.sort(Lottery(opt_3)))


# In[26]:


# Leaves us with 3 options -- you decide which will lead to the $$$
print('Option 1:', np.sort(Lottery(opt_1)))
print('Option 2:', np.sort(Lottery(opt_2)))
print('Option 3:', np.sort(Lottery(opt_3)))

