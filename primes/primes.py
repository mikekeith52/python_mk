
known_primes=[1,2]
N = 100000

def print_primes():
	""" prints all prime numbers between 1 and global N
		the goal is to make this as memory efficient as possible so that large numbers can be tested
		a prime number is not evenly deivisible by any integer other than 1 and itself
		to speed this up, only test the divisibility of each number against a set of known prime numbers
		when you learn that a number is prime, append it to the list and continue on through each iteration
		prints all primes between 1 and 10,000 in .5 secs on my laptop
		between 1 and 100,000 in 23.8 secs
	"""
	global known_primes
	initial_primes = known_primes.copy()

	class Prime(int):
		def __init__(self,known_primes):
			self.known_primes = known_primes
		def no_negatives(self):
			if self < 1:
				raise TypeError('positive integers value 1 or greater only please')
			return self
		def isNextPrime(self):
			""" meant to check the next prime number after the set of known prime numbers
			    example: when checking 5, it only checks divisibility against 1,2,3 not 4
			"""
			return len([e for e in known_primes if self % e == 0]) == 1 # every number is divisible by 1
		def isKnownPrime(self):
			return self in known_primes

	for i in range(max(initial_primes)+1,N+1):
		if (Prime(i).isNextPrime()):
			known_primes.append(i)
	print(*known_primes,sep='\n')

print_primes()