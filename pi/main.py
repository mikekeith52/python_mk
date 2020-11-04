import math
import numpy as np

pos = 5

def main():
	pi_rnd = np.round(math.pi,pos)
	
	pi_apprx = 0
	j = 0 # jumps
	i = 0 # numeric iterations
	
	while np.round(pi_apprx,pos) != pi_rnd:
		if i % 2 != 0:
			if j % 2 == 0:
				pi_apprx += 4/i
			else:
				pi_apprx -= 4/i
			j+=1
		i+=1

	print('pi rounded to {} decimal places: {}'.format(pos,pi_rnd))
	print('iterations needed to approximate pi correctly to {} decimal places: {:,}'.format(pos,j))
	print(pi_rnd)

if __name__ == '__main__':
	main()
