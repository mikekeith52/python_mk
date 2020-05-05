import pandas as pd
import numpy as np
import tqdm
from itertools import product
from sklearn.ensemble import RandomForestClassifier

# Random Forest Classifier
hyper_params = {
    'max_depth':[10,20],
    'n_estimators':[100,500,1000],
    'min_samples_split':[2,4,6],
    'max_features':['auto','sqrt'],
    'max_samples':[0.5,.99]
}

def wrapper(X_train,y_train,cv=3):

    # expand grid to get all possible combos
    def expand_grid(dictionary):
        """ takes a dictionary of lists, and expands out arrays into a pandas dataframe
        """
        return pd.DataFrame([row for row in product(*dictionary.values())], 
                           columns=dictionary.keys()

    # create cross validate function
    def cross_validate_rf(X_train,y_train,k=3,grid=grid,loss='gini'):
        """ cross validates across k folds
            uses non-sepcified random states, so results can change each time
            returns two outputs: the optimal hyperparameters and the full grid with derived error metrics
        """
        # copy our grid to write error metrics into it
        hyper_grid = grid.copy()
        
        # create the error columns for each cross-validation fold
        for i in range(1,k+1):
            hyper_grid[f'error_{i}'] = 0
        
        # run the random forest estimator through the gird of parameters and score each cv fold
        for i, row in tqdm(hyper_grid.iterrows()):
            rf = RandomForestClassifier(
                n_estimators = row['n_estimators'],
                max_depth = row['max_depth'],
                min_samples_split = row['min_samples_split'],
                max_features = row['max_features'],
                max_samples = row['max_samples']
            )
            errors = 1 - cross_val_score(rf, X_train, y_train, cv=k, scoring = 'accuracy')
            # write each cv score to its own column
            for idx, e in enumerate(errors):
                hyper_grid.loc[hyper_grid.index==i,f'error_{idx+1}'] = e
        # take the mean of each cross-validated iteration to get the final error metric for each line of hyper parameters
        hyper_grid['total_error'] = hyper_grid[[e for e in hyper_grid.columns if e.startswith('error_')]].mean(axis=1)
        min_error = hyper_grid['total_error'].min()
        # return the row with the lowest error metric as well as the full set of results
        return hyper_grid.loc[hyper_grid['total_error'] == min_error], hyper_grid
        
    grid = expand_grid(hyper_params)
    cross_validate_rf(X_train,y_train,k=cv,grid=grid,loss='gini')
