## Imporint libraries
import sys
import os
import dill as pickle
import numpy as np
import pandas as pd
from sklearn import metrics ## For loss functions
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier

### Running Extra trees
def runET(train_X, train_y, test_X, test_y=None, test_X2=None, rounds=100, depth=20, 
          leaf=10, feat=0.2,min_data_split_val=2,seed_val=0,job = -1):
	model = ExtraTreesClassifier(
                    n_estimators = rounds,
					max_depth = depth,
					min_samples_split = min_data_split_val,
					min_samples_leaf = leaf,
					max_features =  feat,
					n_jobs = job,
					random_state = seed_val)
	model.fit(train_X, train_y)
	train_preds = model.predict_proba(train_X)[:,1]
	test_preds = model.predict_proba(test_X)[:,1]
	
	test_preds2 = 0
	if test_X2 is not None:
		test_preds2 = model.predict_proba(test_X2)[:,1]
	
	test_loss = 0
	if test_y is not None:
		train_loss = metrics.roc_auc_score(train_y, train_preds)
		test_loss = metrics.roc_auc_score(test_y, test_preds)
		print("Depth, leaf, feat : ", depth, leaf, feat)
		print("Train and Test loss : ", train_loss, test_loss)
	return test_preds, test_loss, test_preds2, model

def label_encoder(df,columns):
    '''
    Function to label encode
    Required Input - 
        - df = Pandas DataFrame
        - columns = List input of all the columns which needs to be label encoded
    Expected Output -
        - df = Pandas DataFrame with lable encoded columns
        - le_dict = Dictionary of all the column and their label encoders
    '''
    le_dict = {}
    for c in columns:
        print("Label encoding column - {0}".format(c))
        lbl = LabelEncoder()
        lbl.fit(list(df[c].values.astype('str')))
        df[c] = lbl.transform(list(df[c].values.astype('str')))
        le_dict[c] = lbl
    return df, le_dict

def holdout_cv(X,y,size = 0.3, seed = 1):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = size, random_state = seed)
    X_train = X_train.reset_index(drop='index')
    X_test = X_test.reset_index(drop='index')
    return X_train, X_test, y_train, y_test

data = np.genfromtxt('./data/adult.data.txt', delimiter=', ', dtype=str)
feature_names = [
    "Age", "Workclass", "fnlwgt", "Education", "Education-Num",
    "Marital Status", "Occupation", "Relationship", "Race", "Sex",
    "Capital Gain", "Capital Loss", "Hours per week", "Country", 'income'
]
data = pd.DataFrame(data)
data.columns = feature_names
data.head()

## Separating train and test data 80:20
test_indices = np.random.randint(0,data.shape[0],size = int(data.shape[0]/5))
test_data = data.loc[test_indices,:].reset_index(drop=True)
train_data = data.loc[set(range(data.shape[0]))-set(test_indices),:].reset_index(drop=True)

## Data processing

## Defining numerical variables
numerical_features = list(data.columns[[0,2,4,10,11,12]])

## Defining categorical variables
categorical_features = list(data.columns[[1,3,5,6,7,8,9,13]])

## Converting numerical feature data type to float
for i in numerical_features:
    train_data.loc[:,i] = train_data.loc[:,i].astype(float)

## creating a target variable
y_label = list(train_data.income.apply(lambda x: 1 if x == '>50K' else 0))
train_data.drop(['income'],axis = 1, inplace=True)

## One hot encoding categorical features
data_processed, le_dict = label_encoder(train_data,categorical_features)
data_processed.head()

## Creating hold-out CV
X_train, X_test, y_train, y_test = holdout_cv(data_processed,y_label,size =0.3)
X_train = X_train.reset_index(drop='index')
X_test = X_test.reset_index(drop='index')

## Model building 
## Running an logistic regression model 
pred_y_test, loss,_,et_model = runET(X_train, y_train, X_test, y_test, rounds=200)

et_model_package = {'numerical_features' : numerical_features,
                    'label_encoders' : le_dict,
                    'model':et_model}

## Numerical column names
pickle.dump(et_model_package,open('./models/et_model_package_'+str(round(loss,3))+'.p','wb'))