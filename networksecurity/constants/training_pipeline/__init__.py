import os
import numpy as np


'''
Constants related to Data Ingestion
'''
DATA_INGESTION_DATABASE_NAME:str="network-security"
DATA_INGESTION_COLLECTION_NAME:str="phishingData"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float= 0.2

'''
defining common constant variable for training pipeline
'''
TARGET_COLUMN = "Result"
PIPELINE_NAME="NetworkSecurity"
ARTIFACT_DIR="Artifacts"
FINAL_DIR="final_model"
FILE_NAME="dataset.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")
SAVED_MODEL_DIR = os.path.join("saved_models")

'''
Constants related to Data Validation
'''
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALIDATED_DIR:str="validated"
DATA_VALIDATION_INVALIDATED_DIR:str="invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str= "report.yaml"

'''
Constants related to Data Transformation
'''
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
## KNN imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
  "missing_values": np.nan,
  "n_neighbors": 3,
  "weights": "uniform"
}


'''
Constants related to Model Trainer
'''
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05