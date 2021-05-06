import random
import matplotlib.pyplot as plt

def main():
	i = random.randint(1,100_000_000)
	print('beggining int: {:0,d}'.format(i))
	seq = []
	while True:
		seq.append(i)
		if i == 1:
			print(f'ended in {len(seq)} iterations')
			plt.plot(seq)
			plt.xlabel('iteration')
			plt.ylabel('value')
			plt.savefig('img.jpg')
			plt.show()
			exit(0)
		elif i % 2 == 0:
			i= i/2
		else:
			i = i*3+1

if __name__ == '__main__':
	main()