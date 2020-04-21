def interact_cols(X,which='all',drop=None):
    """ given a pandas dataframe of predictor variables (X), choose columns to interact
        by default, this will interact all columns, but you can change parameter which to a dictionary where key is one columns and value is other
        the column name will be the two original column names separated by a *
        you can perform a triple interaction by ordering the dictionary correctly (columns will be placed in order they appear in dictionary)
        you can then pass the interactions through the rfe module to whittle down predictors and arrive at the most powerful model
        drop is a list of interactions to drop after the interactions have been run (example: you want to drop only a copule interacted columns and use which = "all" instead of writing a really long dictionary)
        drop must be a list or str type
    """

    if which == 'all':
        first_len = len(X.columns)
        for i, col in enumerate(X.columns):
            i+=1
            while i < first_len:
                X[f'{col}*{X.columns[i]}'] = X[col]*X[X.columns[i]]
                i+=1
    elif isinstance(which,list):
        for t in which:
            X[f'{t[0]}*{t[1]}'] = X[t[0]]*X[t[1]]
    else:
        raise TypeError('which should be "all" or a list of tuples')

    if isinstance(drop,(str,list)):
        X.drop(columns=drop,inplace=True)