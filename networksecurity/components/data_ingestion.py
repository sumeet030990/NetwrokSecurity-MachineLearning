from networksecurity.exception.exception import CustomException
from networksecurity.logging import logger
import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.constants import training_pipeline

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')

class DataIngestion:
  def __init__(self, data_ingestion_config: DataIngestionConfig):
    try:
      self.data_ingestion_config = data_ingestion_config
    except Exception as e:
      raise CustomException(e,sys)
  
  '''
  Step1: fetch data from mongo
  '''
  def fetch_data_from_mongo(self):
    try:
      database_name=self.data_ingestion_config.database_name
      collection_name = self.data_ingestion_config.collection_name
      
      self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

      collection = self.mongo_client[database_name][collection_name]

      df=pd.DataFrame(list(collection.find()))

      # drop _id column as if is neccessary
      if "_id" in df.columns.to_list():
        df = df.drop(columns=["_id"], axis=1)
      
      df.replace({"na":np.nan}, inplace=True)

      return df
    
    except Exception as e:
      raise CustomException(e,sys)

  '''
  Step2: save data to feature store
  '''  
  def store_data_to_feature_store(self, dataframe: pd.DataFrame):
    try:
      feature_store_file_path = self.data_ingestion_config.feature_store_file_path

      ## creating folder
      dir_path  = os.path.dirname(feature_store_file_path)
      os.makedirs(dir_path,exist_ok=True)

      dataframe.to_csv(feature_store_file_path, index=False, header=True)

      return dataframe
    except Exception as e:
      raise CustomException(e,sys)
  
  '''
  Step3: train test split the dataframe in training and testing
  '''
  def train_test_split_df(self, dataframe: pd.DataFrame):
    try:
      train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

      dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

      os.makedirs(dir_path, exist_ok=True)

      train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)

      test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
    except Exception as e:
      raise CustomException(e,sys)
    

  '''
  Initiate Data Ingestion
  '''
  def initiate_data_ingestion(self):
    try:
      df = self.fetch_data_from_mongo() ## Step1
      df = self.store_data_to_feature_store(df) ## Step2: Store the dat from mongo to csv(better practice)

      self.train_test_split_df(df) ## Step3: divide the data in training and testing

      dataIngestionArtifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)

      print(dataIngestionArtifact)
      return dataIngestionArtifact

    except Exception as e:
      raise CustomException(e,sys)
