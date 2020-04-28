import pandas as pd
from pivot import pivot
import math

def main():
	"""
	"""
	def quarter(month):
		""" takes a month and returns the corresponding quarter
		"""
		return math.ceil(month/3)

	data = pd.read_csv('data/cogsley_sales.csv')
	data['year'] = data['OrderDate'].apply(lambda x: int(x.split('-')[0]))
	data['month'] = data['OrderDate'].apply(lambda x: int(x.split('-')[1]))
	data['quarter'] = data['month'].apply(lambda x: quarter(x))

	pivot_tbl_3x2 = pivot(data,rows=['Industry','CompanyName','ProductCategory'],cols=['quarter','year'],metric='SaleAmount')
	pivot_tbl_2x2 = pivot(data,rows=['ProductCategory','ProductKey'],cols=['quarter','year'],metric='SaleAmount')
	with pd.ExcelWriter('output/PivotOutput.xlsx', engine='xlsxwriter') as writer:
		pivot_tbl_3x2.to_excel(writer,sheet_name='Industry_Pivot')
		pivot_tbl_2x2.to_excel(writer,sheet_name='Product_Pivot')

	

if __name__ == '__main__':
	main()
