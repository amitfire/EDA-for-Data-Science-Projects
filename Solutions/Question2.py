
from sklearn.preprocessing import OneHotEncoder
def check_encoding(df):
    
    cat_cols = df.select_dtypes(include='object') # Assuming that all the categorical columns will have data types as object
    
    df = df.drop(df.columns[0],axis=1)
    cat_col = df.select_dtypes(include='object')
    con_col = df.select_dtypes(exclude='object')
    
    for col in df.columns:
        if col in con_col:
            pass
        elif col in cat_col and df[col].nunique()<20:
            df_one = df
            df_one_hot = pd.get_dummies(df_one,drop_first=True)
            return df_one_hot
        elif col in cat_col and df[col].nunique()>20:
            
            #calculate supervised ratio or WOE as per target .
            #When predicting churn for example, a person whose ZIP code is 10009 will be given a transformed value of 
            #the percentage of churners in that ZIP code. So if the training set consists of 100 customers in ZIP code 10009, 5 of which churned (so Pi=5 and Ni=95) then the transformed value is 0.05.          
            # changing categorical variable into monotonous continuous variable.
            # value will be same for same categorical variable.
            # output interpretation will also be easy.
            
            

check_encoding()