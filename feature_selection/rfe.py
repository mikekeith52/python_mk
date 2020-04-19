from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression


def rfe(X,y,model_type="logistic",keep='auto',print_support=True,print_rankings=False):
    """ recursive feature elimination
        from the sklearn documentation: 
	Given an external estimator that assigns weights to features (e.g., the coefficients of a linear model), the goal of recursive feature elimination (RFE) is to select features by recursively considering smaller and smaller sets of features.
	First, the estimator is trained on the initial set of features and the importance of each feature is obtained either through a coef_ attribute or through a feature_importances_ attribute. 
	Then, the least important features are pruned from current set of features. That procedure is recursively repeated on the pruned set until the desired number of features to select is eventually reached.
	X and y should be your predictors and dependent variable in pandas dataframe format.
	Returns the reduced set of columns to use in your model.
        model_type supports the following values: 'logistic' or 'linear'
        keep will take 'auto' or a positive integer value -- if an integer, this will return the top however many predictors that are best according to RFE
    """

    if model_type == 'logistic':
	   model = LogisticRegression()
    elif model_type == 'linear':
        model = LinearRegression()
    else:
        rasie TypeError("don't know which model to pick!")

	rfe = RFE(model)
	rfe = rfe.fit(X, y.values.ravel())

	# should we keep each column according to the rfe?
	if print_support:
			for i, col in enumerate(X.columns):
			    print({col:rfe.support_[i]})

    # what is each column's rank according to the RFE?
    if print_rankings:
        for i, col in enumerate(X.columns):
            print({col:rfe.ranking_[i]})
            
    # create a list of columns to use in model
    if keep == 'auto':
        rfe_cols = [X.columns[i] if e for i,e in enumerate(rfe.support_)]
    elif isinstance(keep,int) & (keep > 0):
        rfe_cols = X.columns[:keep].to_list()
    else:
        raise TypeError('keep must be "auto" or a positive integer')

    return rfe_cols
