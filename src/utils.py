import pandas as pd
import numpy as np
import dill
import os
import sys
import pickle

from src.exception import CustomException
from src.logger import logging

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,"wb") as file:
            pickle.dump(obj,file)
    except Exception as e:
        logging.error(f"Failed to save the object at {file_path}")
        raise CustomException(e,sys)
            