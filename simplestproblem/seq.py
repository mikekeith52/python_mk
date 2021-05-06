import matplotlib.pyplot as plt
import seaborn as sns

seq = range(1,100_000)

x = []
y = []

def main():
	for i in seq:
		c = 0
		x.append(i)
		while True:
			c += 1
			if i == 1:
				y.append(c)
				break
			elif i % 2 == 0:
				i= i/2
			else:
				i = i*3+1

	sns.regplot(x=x,y=y,fit_reg=True,scatter=True)
	plt.xlabel('starting int')
	plt.ylabel('iterations to finish')
	plt.savefig('pattern.jpg')
	plt.show()

if __name__ == '__main__':
	main()