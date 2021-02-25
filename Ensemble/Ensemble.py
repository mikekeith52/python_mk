import numpy as np

class Ensemble:
    """ averages results from several sklearn models
    """
    def __init__(self,models):
        """ models : a list of fitted sklearn model objects
        """
        self.models = models
        
    def fit(self,X,y,refit=True):
        """ placeholder for eli5
        """
        if refit:
            for m in self.models:
                m.fit(X,y)
        else:
            pass
        
    def score(self,X,y):
        scores = []
        for m in self.models:
            scores.append(m.score(X,y))
        return np.array(scores).mean(axis=0)
            
    def predict_proba(self,X):
        predp0 = []
        predp1 = []
        for m in self.models:
            predp0.append(list(m.predict_proba(X)[:,0]))
            predp1.append(list(m.predict_proba(X)[:,1]))
        predp0 = np.array(predp0).mean(axis=0)
        predp1 = np.array(predp1).mean(axis=0)
        self.predp = np.array([[p0,p1] for p0,p1 in zip(predp0,predp1)])
        return self.predp
    
    def predict(self,X):
        self.predict_proba(X)
        return self.predp[:,1].round()
