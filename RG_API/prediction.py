from flask.app import Flask
import numpy as np
import pandas as pd

import config as cf

def predict(data, model):
    data = data["inputdata"]
    pred_label = "not eligible for discount"
    eligibility_flag = False
    input_data = pd.DataFrame(data, index=[0])
    print(input_data)
    print(model.predict_proba(input_data))
    pred_prob = model.predict_proba(input_data).max()
    print(pred_prob)
    pred_class = model.predict(input_data)
    print(pred_class)

    if pred_class != 2:
        pred_label = "eligible for discount"
        eligibility_flag = True

    return pred_label, str(pred_class[0]), str(pred_prob), eligibility_flag
