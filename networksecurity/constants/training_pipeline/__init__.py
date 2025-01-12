import os


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
FILE_NAME="dataset.csv"

TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
