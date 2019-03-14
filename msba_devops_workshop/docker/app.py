#requests are objects that flask handles (get set post, etc)
from flask import Flask, request, jsonify
## Importing required libraries
import os, sys
## For DataFrame operation
import pandas as pd
## Numerical python for matrix operations
import numpy as np 
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import dill as pickle

#initalize our flask app
app = Flask(__name__)

## Loading serialized model, preprocessor and numerical_feature list
rf_model = pickle.load(open('./model/rf_model.p','rb'))
numerical_features = pickle.load(open('./model/numerical_list.p','rb'))
le_dict = pickle.load(open('./model/le_dict.p','rb'))


@app.route('/predict', methods=['POST'])
def apicall():
    """
    API Call 
    Pandas dataframe (sent as a payload) from API Call
    """
    try:
        test_json = request.get_json()
        test = pd.read_json(test_json, orient='records')
        
        ## Preprocessing step
        
        ## Converting numerical feature data type to float
        for num_column in numerical_features:
            test.loc[:,num_column] = test.loc[:,num_column].astype(float)
        
        ## Label encoding features for columnar data
        for key in le_dict.keys():
            lbl = le_dict[key]
            test[key] = lbl.transform(list(test[key].values.astype('str')))
            
    except Exception as e:
        raise e
    if test.empty:
        return(bad_request())
    else:
        ## Predicting for test data
        print(test.shape[0])
        predictions = pd.DataFrame({'predictions': rf_model.predict_proba(test)[:,1]})
        predictions['index'] = range(predictions.shape[0])
        ## Returning response
        responses = jsonify(predictions=predictions.to_json(orient="records"))
        responses.status_code = 200
        
        return (responses)
        
if __name__ == "__main__":
	#decide what port to run the app in
	#port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	#app.run(host='localhost', port=port)
	app.run(host='0.0.0.0', port=80)