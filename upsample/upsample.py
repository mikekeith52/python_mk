from imblearn.over_sampling import SMOTE

def upsample(X_train,y_train):
	""" balances a dataset (where dependent variables is 0/1) to increase accuracy in models
	    returns oversampled X matrix and oversampled y array
	"""

	# training conditions
	os = SMOTE(random_state=20)
	# upsample
	return os.fit_sample(X_train, y_train)