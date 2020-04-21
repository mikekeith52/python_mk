import pandas as pd
from pivot import pivot

def main():
	"""
	"""
	def quarter(month):
		"""
		"""
		if month in (1,2,3):
			return 1
		elif month in (4,5,6):
			return 2
		elif month in (7,8,9):
			return 3
		elif month in (10,11,12):
			return 4

	data = pd.read_csv('data/cogsley_sales.csv')
	data['year'] = data['OrderDate'].apply(lambda x: int(x.split('-')[0]))
	data['month'] = data['OrderDate'].apply(lambda x: int(x.split('-')[1]))
	data['quarter'] = data['month'].apply(lambda x: quarter(x))

	pivot_tbl_3x2 = pivot(data,rows=['Industry','CompanyName','ProductCategory'],cols=['quarter','year'],metric='SaleAmount')
	pivot_tbl_3x2.to_excel('output/test.xlsx')

	#pivot_tbl_2x2_f = format_2x2(pivot_tbl_2x2)
	#pivot_tbl_3x2_f = format_3x2(pivot_tbl_3x2)

if __name__ == '__main__':
	main()
