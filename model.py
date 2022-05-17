"""
    Helper functions for the pretrained model to be used within our API.
    Author: Explore Data Science Academy.
    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    Importantly, you will need to modify this file by adding
    your own data preprocessing steps within the `_preprocess_data()`
    function.
    ----------------------------------------------------------------------
    Description: This file contains several functions used to abstract aspects
    of model interaction within the API. This includes loading a model from
    file, data preprocessing, and model prediction.  
"""

# Helper Dependencies
import numpy as np
import pandas as pd
import pickle
import json

def _preprocess_data(data):
    """Private helper function to preprocess data for model prediction.
    NB: If you have utilised feature engineering/selection in order to create
    your final model you will need to define the code here.
    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.
    Returns
    -------
    Pandas DataFrame : <class 'pandas.core.frame.DataFrame'>
        The preprocessed data, ready to be used our model for prediction.
    """
    # Convert the json string to a python dictionary object
    feature_vector_dict = json.loads(data)
    # Load the dictionary as a Pandas DataFrame.
    df = pd.DataFrame.from_dict([feature_vector_dict])

    # ---------------------------------------------------------------
    # NOTE: You will need to swap the lines below for your own data
    # preprocessing methods.
    #
    # The code below is for demonstration purposes only. You will not
    # receive marks for submitting this code in an unchanged state.
    # ---------------------------------------------------------------

    # ----------- Replace this code with your own preprocessing steps --------
    df_clean = df[['time','Madrid_wind_speed', 'Valencia_wind_deg', 'Valencia_wind_speed',
       'Seville_humidity', 'Bilbao_wind_speed', 'Barcelona_pressure',
       'Bilbao_pressure', 'Madrid_pressure', 'Valencia_humidity',
       'Barcelona_temp', 'Bilbao_temp', 'Madrid_temp']]
    df_clean['time'] = pd.to_datetime(df_clean['time'])
    df_clean['Valencia_wind_deg'] = df_clean.Valencia_wind_deg.str.extract('(\d+)')
    df_clean['Valencia_wind_deg'] = pd.to_numeric(df_clean['Valencia_wind_deg'])


    # create new features
    df_clean['year'] = df_clean['time'].dt.year
    df_clean['month'] = df_clean['time'].dt.month
    df_clean['day'] = df_clean['time'].dt.day
    df_clean['hour'] = df_clean['time'].dt.hour
    df_clean['weekday'] = df_clean['time'].dt.weekday
    df_clean = df_clean.drop('time', axis=1) 

    #fill any missing value with mean of that column
    df_clean = df_clean.fillna(df_clean.mean())
    # ------------------------------------------------------------------------

    return df_clean

def load_model(path_to_model:str):
    """Adapter function to load our pretrained model into memory.
    Parameters
    ----------
    path_to_model : str
        The relative path to the model weights/schema to load.
        Note that unless another file format is used, this needs to be a
        .pkl file.
    Returns
    -------
    <class: sklearn.estimator>
        The pretrained model loaded into memory.
    """
    return pickle.load(open(path_to_model, 'rb'))


""" You may use this section (above the make_prediction function) of the python script to implement 
    any auxiliary functions required to process your model's artifacts.
"""

def make_prediction(data, model):
    """Prepare request data for model prediction.
    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.
    model : <class: sklearn.estimator>
        An sklearn model object.
    Returns
    -------
    list
        A 1-D python list containing the model prediction.
    """
    # Data preprocessing.
    prep_data = _preprocess_data(data)
    # Perform prediction with model and preprocessed data.
    prediction = model.predict(prep_data)
    # Format as list for output standardisation.
    return prediction[0].tolist()