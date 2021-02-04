import numpy as np

class Ensemble:
    def __init__(self,_models_):
        """ _models_ : a list of fitted sklearn model objects
        """
        self.models = _models_
        
    def fit(self,X,y):
        """ placeholder for eli5
        """
        pass
        
    def score(self,X,y):
        scores = []
        for m in self.models:
            scores.append(m.score(X,y))
        return np.array(scores).mean(axis=0)
            
    def predict_proba(self,X):
        self.predp = []
        for m in self.models:
            self.predp.append(list(m.predict_proba(X)[:,1]))
        self.predp = np.array(self.predp).mean(axis=0)
        return self.predp
    
    def predict(self,X,cutoff=.5):
        self.predict_proba(X)
        return np.where(self.predp >= cutoff,1,0)