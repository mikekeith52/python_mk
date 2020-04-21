import pandas as pd
import numpy as np
import warnings

def pivot(data,rows,cols,metric,function=np.sum,subtotals=True):
	assert(isinstance(rows,list))
	assert(isinstance(cols,list))
	if subtotals:
		if len(rows) == 2:
			output_stg1 = pd.pivot_table(data,index=rows,columns=cols,aggfunc=function,values=metric)
			output_stg2 = pd.concat([
					  idx1.append(idx1.sum().rename((idx0,'000')))
					  for idx0, idx1 in output_stg1.groupby(level=0)
					 ]).append(output_stg1.sum().rename(('00', 'Grand Total')))
			output_stg2.sort_index(axis=0,inplace=True)
			output_stg2.rename(index={'00':'Overall'},level=0,inplace=True)
			output_stg2.rename(index={'000':'Total'},level=1,inplace=True)
			output = output_stg2.sort_index(axis=1)

		elif len(rows) == 3:
			output_stg1 = pd.pivot_table(data,index=rows,columns=cols,aggfunc=function,values=metric)
			# first loop to keep track of how many level 1s for each level 0 (to avoid writing out a total that only totals one other line)
			index_counter={}
			for i in output_stg1.index.get_level_values(0).unique():
				for j in output_stg1.loc[i].index.get_level_values(0):
					if f'{i},{j}' not in index_counter.keys():
						index_counter[f'{i},{j}'] = 1
					else:
						index_counter[f'{i},{j}'] += 1

			# second loop to write totals for each level 1
			for i in output_stg1.index.get_level_values(0).unique():
				for j in output_stg1.loc[i].index.get_level_values(0).unique():
					output_stg1.loc[(i,j,'001')] = output_stg1.loc[(i,j)].sum()
					# drop when there is only one other level 1 and leave only the total
					if index_counter[f'{i},{j}']==1:
						for k in output_stg1.loc[(i,j)].index.get_level_values(0).unique():
							if k != '001':
								output_stg1.drop(index=(i,j,k),inplace=True)

			# now for writing out level 0 totals without double counting
			output_stg2 = pd.concat([
						  idx1.append(idx1.sum().rename((idx0,'001'+idx0,'000')))
						  for idx0, idx1 in output_stg1.iloc[output_stg1.index.get_level_values(rows[-1]) == '001'].groupby(level=0)
						  ]).append([
						  output_stg1.iloc[output_stg1.index.get_level_values(rows[-1]) != '001'] # skip the level 1 subtotals to avoid double-counting
						  ]).append(output_stg1.iloc[output_stg1.index.get_level_values(rows[-1]) == '001'].sum().rename(tuple(['00','','000']))) # grand total
			output_stg2.fillna(0,inplace=True)
			output_stg2.sort_index(axis=0,level=0,inplace=True) # this is where all the weird naming conventions pay off
			output_stg2.rename(index={'001':'Total','000':'Grand Total'},level=2,inplace=True) # now everything is where it should be -- rename
			output_stg2.rename(index={'00':'Overall'},level=0,inplace=True)
			for idx0, idx1 in output_stg2.groupby(level=0):
				output_stg2.rename(index={'001'+idx0:idx0},level=1,inplace=True)

			output = output_stg2.sort_index(axis=1)
		else: # use pandas default
			if len(rows) > 3:
				warnings.warn('subtotals only supported at row indices 2 or 3 -- using the default pandas margins for everything else')
			output = pd.pivot_table(data,index=rows,columns=cols,aggfunc=function,margins=True,values=metric)

	else:
		output = pd.pivot_table(data,index=rows,columns=cols,aggfunc=function,values=metric)

	return output



