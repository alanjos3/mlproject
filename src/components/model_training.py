import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, evaluate_model


@dataclass
class ModelTrainingConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl") 
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()
        
    def initiate_model_trainer(self, train_arr,test_arr):
        try:
            logging.info("Initiating Model Training")
            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1])
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "AdaBoost": AdaBoostRegressor(),
                "XGBoost": XGBRegressor(),
                "CatBoost": CatBoostRegressor(),
            }
            
            model_report = evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)
            
            best_model_score = max(sorted(model_report.values()))
            
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                logging.error("Best Model Score is less than 0.6")
                raise CustomException("Best Model Score is less than 0.6",sys)
            
            save_object(self.model_trainer_config.trained_model_file_path, best_model)
            
            predicted = best_model.predict(X_test)
            r2 = r2_score(y_test,predicted)
            return r2
            
        except Exception as e:
            raise CustomException(e,sys)
        
        