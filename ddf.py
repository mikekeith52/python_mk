
class ddf(pd.core.frame.DataFrame):
    """ pandas dataframe with two extra methods
        dummy for creating 0/1 binary variables
        impute_na which uses K Nearest Neighbor to fill in NA values
    """
    def dummy(self,col,exclude_values=[],drop_na=False,exclude_na_levels=False,na_levels=np.NaN,keep_original_col=False,sep=":"):
        """ creates dummy (0/1 variable)
            col is the column you want dummied -- will return as many columns as there are unique values in the column so choose carefully
            exclude_values is a lit of values in that column you want ignored when making dummy columns, you can make this your excluded level
            drop_na is if you want null values droped -- if True, will reduce the number of rows in your dataframe
            exclude_na_levels is if you want your na_levels ignored (meaning no dummy will be made for them)
            na_levels is a user-defined NA level (you can tell it what you want considered null, such as "nan")
            keep_original_col -- if False, the column being dummied will disappear
            sep is how you want the new column names separated (new column name will be the old column name + sep + unique value)
        """
        pd.options.mode.chained_assignment = None
        if drop_na == True:
            self = self.loc[self[col].isnull() == False]
        else:
            self[col].loc[self[col].isnull() == True] = na_levels
            if exclude_na_levels == True:
                exclude_values.append(na_levels)

        self[col] = self[col].astype(str)

        for val in self[col].unique():
            if not val in exclude_values:
                self[f'{col}{sep}{val}'] = 0
                self[f'{col}{sep}{val}'].loc[self[col] == val] = 1

        if keep_original_col == False:
            self.drop(columns=[col],inplace=True)

    def impute_na(self,col,exclude=[]):
        """ uses K-nearest neighbors to fill in missing values
            automatically decides which columns (numerics only) to use as predictors
            a better way to do this is Midas, but this is quick and easy
        """
        predictors=[e for e in self.columns if len(self[e].dropna())==len(self[e])] # predictor columns can have no NAs
        predictors=[e for e in predictors if e != col] # predictor columns cannot be the same as the column to impute (this should be taken care of in the line above, but jic)
        predictors=[e for e in predictors if self[e].dtype in (np.int32,np.int64,np.float32,np.float64,int,float)] # predictor columns must be numeric -- good idea to dummify as many columns as possible
        predictors=[e for e in predictors if e not in exclude] # manually exclude columns (like a dep var)
        clf = KNeighborsClassifier(3, weights='distance')

        df_complete = self.loc[self[col].isnull()==False]
        df_nulls = self.loc[self[col].isnull()]

        trained_model = clf.fit(df_complete[predictors],df_complete[col])
        imputed_values = trained_model.predict(df_nulls[predictors])
        df_nulls[col] = imputed_values

        self[col] = df_complete[col].append(df_nulls[col],ignore_index=False) # preserve index order

    def dummy_regex(self,col,regex_expr=[],sep=':r:'):
        """ this creates a dummy (0/1) variable based on if given phrases (regex_expr) is in the col
            regex_expr should be list type
            sep is how the new column name will be separated
        """
        self[col+sep+'|'.join(regex_expr)] = self[col].astype(str).str.contains('|'.join(regex_expr)).astype(int)