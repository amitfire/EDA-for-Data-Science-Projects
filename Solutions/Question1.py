
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.datasets import make_blobs

class clustered_rank():
    
    def __init__(self):
        self.N = 1000
        self.P= 10
        self.S = 5
        self.K = 3
        
    def create_dataset_with_clusters(self,N=None,P=None,S = None,K =None):
         features, clusters = make_blobs(n_samples = N,
                  n_features = P, centers = K,
                  # with .5 cluster standard deviation,
                  cluster_std = 0.4,
                  shuffle = True)
   
         return pd.DataFrame(features)

    def rank_features(self):
        x= create_dataset_with_clusters(self.N,self.P,self.S,self.K)
        pca = PCA(n_components=self.S)
        pca.fit_transform(x)
        print(pca.explained_variance_ratio_)
    
    
c = clustered_rank()
c.rank_features()