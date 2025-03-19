import os
import sys

from src.exception import CustomException
from src.logger import logging
from src.components.data_tranformation import DataTransformation
from src.components.model_training import ModelTrainer
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")
        try:
            data = pd.read_csv("notebook/data/stud.csv")
            logging.info("Read the dataset as a DataFrame")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Saved the raw data")
            
            logging.info("Splitting the data into train and test")
            train_set , test_set = train_test_split(data, test_size = 0.2, random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logging.info("Data Ingestion Completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Data Ingestion Failed")
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_path , test_path = obj.initiate_data_ingestion()
    
    data_transformation= DataTransformation()
    train_arr , test_arr, _ = data_transformation.initiate_data_transformation(train_path, test_path)
    
    model_trainer= ModelTrainer()
    model_trainer.initiate_model_trainer(train_arr, test_arr)
        