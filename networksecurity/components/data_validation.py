from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils import read_yaml_file, write_yaml_file
from networksecurity.exception.exception import CustomException

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys


class DataValidation:
  def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
    try:
      self.data_ingestion_artifact = data_ingestion_artifact
      self.data_validation_config = data_validation_config
      self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    except Exception as e:
      raise CustomException(e, sys)
  
  @staticmethod
  def read_data(file_path)-> pd.DataFrame:
    try:
      return pd.read_csv(file_path)

    except Exception as e:
      raise CustomException(e, sys)
  
  '''
  validate number of columns
  '''
  def validate_number_of_columns(self, dataframe: pd.DataFrame)->bool:
    try:
      number_of_columns = len(self.schema_config)

      if len(dataframe.columns)==number_of_columns:
        return True ## means number of columns are same
      
      return False

    except Exception as e:
      raise CustomException(e, sys)
  
  '''
  check from datadrift i.e if data is transforming from normal deviation to left or right skewed
  '''
  def detect_dataset_drift(self, base_dataframe: pd.DataFrame, current_dataframe: pd.DataFrame, threshold=0.05)->bool:
    try:
      result = True
      report ={}

      for column in base_dataframe.columns:
        d1 = base_dataframe[column]
        d2 = current_dataframe[column]

        ## check for drift using ks_2samp, it compare distribution of two sample
        is_dist_same = ks_2samp(d1,d2)

        if threshold <= is_dist_same.pvalue:
          is_found = False
        else:
          is_found = True
          result = False
        
        report.update({
          column:{
            "p_value": float(is_dist_same.pvalue),
            "drift_staus": is_found
          }
        })

      drift_report_file_path = self.data_validation_config.drift_report_file_path

      #Create directory
      dir_path = os.path.dirname(drift_report_file_path)
      os.makedirs(dir_path,exist_ok=True)

      write_yaml_file(file_path=drift_report_file_path, content=report)

      return result
    except Exception as e:
      raise CustomException(e, sys)
    
  def initate_data_validation(self)->DataValidationArtifact:
    try:
      train_file_path = self.data_ingestion_artifact.trained_file_path
      test_file_path = self.data_ingestion_artifact.test_file_path


      ## read the data from train and test
      train_df = DataValidation.read_data(train_file_path)
      test_df = DataValidation.read_data(test_file_path)

      # validate number of columns
      validate_train_columns = self.validate_number_of_columns(dataframe=train_df)
      if not validate_train_columns:
        error_message = f"Train dataframe does not contains all columns. \n"
      validate_test_columns = self.validate_number_of_columns(dataframe=test_df)
      if not validate_test_columns:
        error_message = f"Test datafra me does not contains all columns. \n"
      

      ## lets check from datadrift i.e if data is transforming from normal deviation to left or right skewed
      status = self.detect_dataset_drift(base_dataframe=train_df, current_dataframe= test_df)

      dir_path = os.path.dirname(self.data_validation_config.valid_training_file_path)
      print(f"dir_path: {dir_path}")
      print("dir_path", dir_path)
      os.makedirs(dir_path, exist_ok=True)

      train_df.to_csv(
        self.data_validation_config.valid_training_file_path, index= False, header=True
      )
      
      test_df.to_csv(
        self.data_validation_config.valid_testing_file_path, index= False, header=True
      )

      data_validation_artifact = DataValidationArtifact(
        validation_status=status,
        valid_trained_file_path=self.data_ingestion_artifact.trained_file_path,
        valid_test_file_path=self.data_ingestion_artifact.test_file_path,
        invalid_train_file_path=None,
        invalid_test_file_path=None,
        drift_report_file_path=self.data_validation_config.drift_report_file_path
      )

      return data_validation_artifact

      
    except Exception as e:
      raise CustomException(e, sys)
