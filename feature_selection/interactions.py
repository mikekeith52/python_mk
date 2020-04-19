def interact_cols(X,which='all',drop=None):
	""" given a pandas dataframe of predictor variables (X), choose columns to interact
		by default, this will interact all columns, but you can change which to a dictionary where key is one columns and value is other
		the column name will be the two original column names separate by a *
		you can perform a triple interaction by ordering the dictionary correctly (columns will be placed in order they appear in dictionary)
		you can then pass the interactions through the rfe module to widdle down predictors
		drop is a list of interactions to drop after the interactions have been run (like if you want to drop columns at the end and use which = "all" instead of writing a really long dictionary)
		drop should be a list or str type
	"""

	if which == 'all':
		for i, col in enumerate(X.columns):
			i+=1
			while i < len(X.columns):
				X[f'{col}*{X.columns[i]}'] = X[col]*X[X.columns[i]]
				i+=1
	elif isinstance(which,dict):
		for key, val in which.items():
			X[f'{key}*{val}'] = X[{key}]*X[val]
	else:
		raise TypeError('which should be "all" or a dictionary of columns in X to interact')

	if isinstance(drop,(str,list)):
		X.drop(columns=drop,inplace=True)