import warnings
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import KFold,cross_val_score,train_test_split


class OnlineRetention():
    def __init__(self,data):
        # global params will be here
        print('Please Use functions for Visualising the Data And Building the Model')
        self.df = pd.read_csv(data)
        self.features = self.df.columns
        self.size = self.df.shape[0]
        self.no_of_features = self.df.shape[1]
        self.cat_col = self.df.select_dtypes(include='object')
        self.con_col = self.df.select_dtypes(exclude='object')
        self.comb = list(itertools.combinations(self.df.select_dtypes(exclude='object'),r=2))
        self.X =  self.df.drop('Revenue',axis=1)
        self.y = self.df['Revenue']
        self.ratio = 0.3
        self.random_st = 25
        
    def get_columns(self):
        return self.df.columns
    
    def get_categorical(self):
        return self.cat_col
    
    def get_continuous(self):
        return self.con_col
    
    def get_missing_values(self):
        
        if self.df.isna().sum().sum()>0:
            print( self.df.isna().sum()//self.size)
            
        else:
            return df.isna().sum().sum()
    
    def get_feature_categories(self):
        return ((self.df.select_dtypes(include='object').value_counts()/self.size)*100)
    
        
    def get_outliers_and_proportion(self):
          cols= self.df.select_dtypes(exclude='object').columns
          dict_ot = {}
          for i in cols:
              q1 = self.df[i].quantile(0.25)
              q3 = self.df[i].quantile(0.75)
              iqr = q3-q1
              upper_limit =  q3 + 1.5 * (iqr)
              lower_limit =  q1- 1.5 * (iqr)
              dict_ot[i] = [self.df[(self.df[i]>upper_limit)|(self.df[i]<lower_limit)].shape[0],round((self.df[(self.df[i]>upper_limit)|(self.df[i]<lower_limit)].shape[0]/self.df.shape[0])*100,2)]
          return(pd.DataFrame(list(dict_ot.items())))
            
    def get_univariate_analysis_categorical(self,cat_col=None):
        if cat_col is None:
            cat_col =self.cat_col
        #cat_col = self.df.select_dtypes(include='object)
        for c in cat_col:
            plt.figure(figsize=(10,5))
            self.df[c].value_counts().plot.bar()
            
    def get_univariate_analysis_continuous(self,con_col =None):
        if con_col is None:
            con_col = self.con_col
        #con_col = self.df.select_dtypes(include='object)
        for c in con_col:
            plt.figure(figsize=(10,5))
            sns.distplot(self.df[c])
    def get_bivariate_analysis_categorical(self,cat_col = None):
        if cat_col is None:
            cat_col =self.cat_col
        #cat_col = self.df.select_dtypes(include='object)
        for col in cat_col:
            df_plot = pd.crosstab(self.df[col], self.df['Revenue'])
            df_plot.div(df_plot.sum(1).astype(float), axis = 0).plot(kind = 'bar', stacked = True, figsize = (15, 5), color = ['lightgreen', 'green'])
            plt.title(f'{col} vs Revenue', fontsize = 30)
            plt.show()
        
    def get_bivariate_analysis_continuous(self,con_col =None):
        if con_col is None:
            con_col =self.cat_col
        for col in con_col:
            sns.scatterplot(self.df[col],self.df['Revenue'])
            plt.title(f'{col} vs Revenue', fontsize = 30)
            plt.show()
    def get_multivariate_analysis(self,comb = None):
        if comb is None:
            comb = self.comb
        for comb in self.comb :
            sns.scatterplot(self.df[comb[0]],self.df[comb[1]],hue = self.df['Revenue'])
            #plt.title(f'{self.df[comb[0]]} vs {self.df[comb[1]} vs Revenue', fontsize = 30)
            plt.show()
        
    def get_scaled_data(self):
         x_par,y_par = self.X,self.y
         sc = StandardScaler()
         feat = x_par.columns
         x_par = x_par.apply(sc.fit_transform(x_par))
         x_par=  pd.DataFrame(x_par,columns=feat)
         return x_par,y_par
     
    def get_split_data(self,ratio=None):
        if ratio is None:
            ratio = self.ratio
        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y, test_size = self.ratio, random_state = self.random_st)
        return (x_train, x_test, y_train, y_test)
    
    def get_correlation(self):
        x_par,y_par = self.get_scaled_data()
        df_scaled = pd.concat([x_par,y_par],axis=1)
        corr = df_scaled.corr()
        sns.heatmap(corr,annot=True)
    
    def get_one_hot_encoded(self):
        df_one = self.df
        df_one_hot = pd.get_dummies(df_one,drop_first=True)
        return df_one_hot
    
    def get_label_encoded(self):
        le = LabelEncoder()
        df_le = self.df
        df_le_encoded = df_le.select_dtypes(include='object').apply(le.fit_transform)
        return df_le_encoded
    
    def get_features_importance(self):
        x_par,y_par = self.get_scaled_data()
        #df_scaled = pd.concat([x_par,y_par],axis=1)
        rf = RandomForestClassifier()
        x_rf= x_par
        y_rf = y_par
        rf.fit(x_rf, y_rf) 
        feature_importances = pd.DataFrame(rf.feature_importances_,index = x_rf.columns,columns=['importance']).sort_values('importance',ascending=False)
        return feature_importances
        
    def get_features_imp_ols(self):
        x_par,y_par = self.get_scaled_data()
        #df_scaled = pd.concat([x_par,y_par],axis=1)
        X = x_par
        y = y_par
        XC= sm.add_constant(X)
        model = sm.OLS(y,XC)
        return model.fit().summary()
    
    def get_models_comparison(X= None,y=None):
        if X is None or y is None:
            X,y = self.X,self.y
            
        
        models = []

        models.append(('LR', LogisticRegression()))
        models.append(('RF',RandomForestClassifier()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))       
        results = []
        names = []
        x=0
        c=0
        for name, model in models:
           warnings.simplefilter("ignore")
           c=0
           kfold = KFold(n_splits=50, random_state=self.random_st)
           cv_results = cross_val_score(model, X, y, cv=kfold, scoring="accuracy")
           results.append(cv_results)
           names.append(name)
           print(name,cv_results.mean(), cv_results.std())
    
        
    #def get_sampled_data()
        
       
    #def get_transformed_data():
        
    
    
    
a= OnlineRetention('C:/Python27/online_shoppers_intention.csv')
d= a.get_columns()
print(d)        
    