import re
import warnings
warnings.filterwarnings('ignore')

import os
import json
import sys
import io
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
# import joblib
# import pickle
import datetime as dt
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from helper import common_helper as chelper
import config as cf
import prediction as p

class VarTypeSelector(BaseEstimator, TransformerMixin):
    
    def __init__(self,vartype,ignore_var):
        self.vartype=vartype
        self.ignore_var=ignore_var
    
    def fit(self,x,y=None):
        return self
    
    def transform(self,X):
        return X.select_dtypes(self.vartype).drop(self.ignore_var,axis=1)

class get_dummies_PipeLineFriendly(BaseEstimator, TransformerMixin):
    
    def __init__(self,freq_cutoff=0):
        self.freq_cutoff=freq_cutoff
        self.var_cat_dict={}
        
    def fit(self,x,y=None):
        data_cols=x.columns
        for col in data_cols:
            k=x[col].value_counts()
            cats=k.index[k>self.freq_cutoff][:-1]
            self.var_cat_dict[col]=cats
        return self
            
    def transform(self,x,y=None):
        dummy_data=x.copy()
        for col in self.var_cat_dict.keys():
            for cat in self.var_cat_dict[col]:
                name=col+'_'+cat
                dummy_data[name]=(dummy_data[col]==cat).astype(int)
            del dummy_data[col]
        return dummy_data


app = Flask(__name__)
cors = CORS(app)

log_file_name = cf.log_file_name_value
chelper.info(log_file_name, '#'*50)

@app.route('/', methods=["GET"])
def home():
    return "<h1>connection is successful<h1>"
# ******************************************************************************
@app.route('/predict', methods=["POST"])
def DiscountEligibilityAPI():
    # print(request.get_json())
    # # get data
    # data = json.loads(request.data)
    # # convert data into dataframe
    # print("DataFrame loading....")
    # data_df = pd.DataFrame(data["inputdata"], index=[0])
    # # data_df = pd.concat([data_df, data_df], ignore_index=True)
    # print(data_df)

    # # x_test=pd.DataFrame(data=data_pipe.transform(data_df),
    # #     columns=data_pipe.get_feature_names())

    # # predictions
    # result = model.predict(data_df[:1])[0]
    # print(result)

    # result_prob = model.predict_proba(data_df[:1])
    # result_prob = result_prob.max()
    # print(result_prob)

    # # result_class = (result < cf.cutoff_value).astype(int)
    
    # # send back to browser
    # output = {'label': str(result), "probability": str(result_prob)}

    # # return data
    # return jsonify(output)

    doc_data = dict()
    doc_data["ResponseCode"] = ""           
    doc_data["Response"] = ""       
    doc_data["ResponseMessage"] = ""

    response_dict = dict()
    response_dict["DiscountEligibility"] = False
    response_dict["Class"] = "2"
    response_dict["Label"] = "not eligilible for discount"
    response_dict["Probability"] = "0"

    curdt_ = dt.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-4]

    try:
        
        print('[INFO]: Request received....................')
        chelper.info(log_file_name,'Request received....................')
        chelper.info(log_file_name, json.loads(request.data))
        request_param = json.loads(request.data)
        print("Request Parameters: ", request_param)
        
        if "inputdata" not in request_param.keys():
            
            message = "Missing Key \"inputdata\" Parameter."
            print("[ERROR]: {0}".format(message))
            doc_data["ResponseCode"] = "999"
            doc_data["Response"] = "BAD REQUEST"
            doc_data["ResponseMessage"] = message
            chelper.info(log_file_name,'Response sent....................')
            chelper.error(log_file_name, (doc_data))
        elif (not isinstance(request_param["inputdata"], dict)) or (len(request_param["inputdata"]) == 0):

            message = "Inappropriate Data in \"inputdata\" Parameter."
            print("[ERROR]: {0}".format(message))
            doc_data["ResponseCode"] = "999"
            doc_data["Response"] = "BAD REQUEST"
            doc_data["ResponseMessage"] = message
            chelper.info(log_file_name,'Response sent....................')
            chelper.error(log_file_name, (doc_data))
        
        else:
            pred_label, pred_class, pred_prob, eligibility_flag = p.predict(request_param, model)
            if eligibility_flag:
                response_dict["DiscountEligibility"] = eligibility_flag
                response_dict["Class"] = pred_class
                response_dict["Label"] = pred_label
                response_dict["Probability"] = pred_prob

                doc_data["ResponseCode"] = "000"
                doc_data["ResponseMessage"] = "SUCCESS"
                doc_data["Response"] = response_dict
                chelper.info(log_file_name,'Response sent....................')
                chelper.info(log_file_name, (doc_data))
            else:
                response_dict["DiscountEligibility"] = eligibility_flag
                response_dict["Class"] = pred_class
                response_dict["Label"] = pred_label
                response_dict["Probability"] = pred_prob

                doc_data["ResponseCode"] = "100"
                doc_data["ResponseMessage"] = "FAILURE"
                doc_data["Response"] = response_dict
                chelper.info(log_file_name,'Response sent....................')
                chelper.info(log_file_name, (doc_data))

    except Exception as ex: 
        # print("[ERROR]: ", ex)
        message = ex 
        doc_data["ResponseCode"] = "999"                             
        doc_data["Response"] = {} # "FAILURE"                        
        doc_data["ResponseMessage"] = message # "FAILURE" #
        print("[ERROR]: {}".format(doc_data))
        chelper.info(log_file_name,'Response sent....................')
        chelper.error(log_file_name, (doc_data))
    
    return jsonify(doc_data)

# ******************************************************************************

if __name__ == '__main__':
    import joblib
    model_path = "model/my_model_pipeline27Sep24.pkl" # cf.model_path
    print(model_path)
    model = joblib.load(open(model_path, "rb"))
    # with open(model_path, "rb") as model_:
    #     model = pickle.load(model_)
    app.run(host='0.0.0.0', port=cf.port_value, debug=True) 
    # app.run(port=5000)